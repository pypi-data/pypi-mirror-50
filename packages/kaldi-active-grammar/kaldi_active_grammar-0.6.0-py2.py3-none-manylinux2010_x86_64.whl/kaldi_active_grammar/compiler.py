#
# This file is part of kaldi-active-grammar.
# (c) Copyright 2019 by David Zurow
# Licensed under the AGPL-3.0, with exceptions; see LICENSE.txt file.
#

import base64, collections, logging, os.path, re, shlex, subprocess
from contextlib import contextmanager

from six import StringIO
import pyparsing as pp

from . import _log, KaldiError
from .utils import debug_timer, lazy_readonly_property, platform, load_symbol_table, symbol_table_lookup, ExternalProcess
import utils
from .wfst import WFST
from .model import Model
import cloud

_log = _log.getChild('compiler')


########################################################################################################################

def run_subprocess(cmd, format_kwargs, description=None, format_kwargs_update=None, **kwargs):
    with debug_timer(_log.debug, description or "description", False), open(os.devnull, 'w') as devnull:
        output = None if _log.isEnabledFor(logging.DEBUG) else devnull
        args = shlex.split(cmd.format(**format_kwargs), posix=(platform != 'windows'))
        _log.log(5, "subprocess.check_call(%r)", args)
        subprocess.check_call(args, stdout=output, stderr=output, **kwargs)
        if format_kwargs_update:
            format_kwargs.update(format_kwargs_update)


########################################################################################################################

class KaldiRule(object):
    def __init__(self, compiler, name, nonterm=True, has_dictation=None):
        """
        :param nonterm: bool whether rule represents a nonterminal in the active-grammar-fst (only False for the top FST?)
        """
        self.compiler = compiler
        self.name = name
        self.nonterm = nonterm
        self.has_dictation = has_dictation

        # id: matches "nonterm:rule__"; 0-based; can/will change due to rule unloading!
        self.id = int(self.compiler.alloc_rule_id() if nonterm else -1)
        if self.id > self.compiler._max_rule_id: raise KaldiError("KaldiRule id > compiler._max_rule_id")
        if self.id in self.compiler.kaldi_rule_by_id_dict: raise KaldiError("KaldiRule id already in use")
        if self.id >= 0:
            self.compiler.kaldi_rule_by_id_dict[self.id] = self

        self.fst = WFST()
        self.fst_compiled = False
        self.matcher = None
        self.active = True
        self.reloading = False

    def __str__(self):
        return "KaldiRule(%s, %s)" % (self.id, self.name)

    filename = property(lambda self: base64.b16encode(self.name) + '.fst')  # FIXME: need to handle unicode?
    filepath = property(lambda self: os.path.join(self.compiler.tmp_dir, self.filename))
    fst_cache = property(lambda self: self.compiler.fst_cache)
    decoder = property(lambda self: self.compiler.decoder)

    def compile_file(self):
        if not self.reloading and self.filename in self.compiler._fst_filenames_set:
            raise KaldiError("KaldiRule fst filename collision %r. Duplicate grammar/rule name %r?" % (self.filename, self.name))
        self.compiler._fst_filenames_set.add(self.filename)

        fst_text = self.fst.fst_text
        if self.fst_cache.is_current(self.filepath, fst_text):
            # _log.debug("%s: Skipped full compilation thanks to FileCache" % self)
            return
        else:
            # _log.debug("%s: FileCache useless; has %s not %s" % (self, self.fst_cache.cache.get(self.filepath), self.fst_cache.hash_data(fst_text)))
            pass

        _log.debug("%s: Compiling %sstate/%sarc/%sbyte fst.txt file to %s" % (self, self.fst.num_states, self.fst.num_arcs, len(fst_text), self.filename))

        if self.compiler.decoding_framework == 'agf':
            self.compiler._compile_agf_graph(compile=True, nonterm=self.nonterm, input_data=fst_text, filename=self.filepath)
        elif self.compiler.decoding_framework == 'otf':
            with open(self.filepath + '.txt', 'wb') as f:
                # FIXME: https://stackoverflow.com/questions/2536545/how-to-write-unix-end-of-line-characters-in-windows-using-python/23434608#23434608
                f.write(fst_text)
            self.compiler._compile_otf_graph(filename=self.filepath)

        self.fst_compiled = True
        self.fst_cache.add(self.filepath, fst_text)
        self.fst_cache.save()

    def load_fst(self):
        grammar_fst_index = self.decoder.add_grammar_fst(self.filepath)
        assert self.id == grammar_fst_index, "add_grammar_fst allocated invalid grammar_fst_index"

    @contextmanager
    def reload(self):
        """Used for modifying a rule in place, e.g. ListRef."""
        self.reloading = True
        self.fst.clear()
        yield
        self.decoder.reload_grammar_fst(self.id, self.filepath)
        self.reloading = False

    def destroy(self):
        """Unloads rule."""
        self.decoder.remove_grammar_fst(self.id)
        self.compiler._fst_filenames_set.remove(self.filename)

        # Adjust other kaldi_rules ids down, if above self.id, then rebuild dict
        other_kaldi_rules = self.compiler.kaldi_rule_by_id_dict.values()
        other_kaldi_rules.remove(self)
        for kaldi_rule in other_kaldi_rules:
            if kaldi_rule.id > self.id:
                kaldi_rule.id -= 1
        self.compiler.kaldi_rule_by_id_dict = { kaldi_rule.id: kaldi_rule for kaldi_rule in other_kaldi_rules }

        self.compiler.free_rule_id()


########################################################################################################################

class Compiler(object):

    def __init__(self, model_dir=None, tmp_dir=None, cloud_dictation=None):
        self.decoder = None
        self.decoding_framework = 'agf'
        assert self.decoding_framework in ('otf', 'agf')
        self.parsing_framework = 'token'
        assert self.parsing_framework in ('text', 'token')

        self.model = Model(model_dir, tmp_dir)

        self._num_kaldi_rules = 0
        self._max_rule_id = load_symbol_table(self.files_dict['phones.txt'])[-1][1] - symbol_table_lookup(self.files_dict['phones.txt'], '#nonterm:rule0')  # FIXME: inaccuracy
        self._max_rule_id = 999
        self.nonterminals = tuple(['#nonterm:dictation'] + ['#nonterm:rule%i' % i for i in range(self._max_rule_id + 1)])

        self.kaldi_rule_by_id_dict = collections.OrderedDict()  # maps KaldiRule.id -> KaldiRule
        self._fst_filenames_set = set()

        self.cloud_dictation = cloud_dictation

        self._compile_base_fsts()

    exec_dir = property(lambda self: self.model.exec_dir)
    model_dir = property(lambda self: self.model.model_dir)
    tmp_dir = property(lambda self: self.model.tmp_dir)
    files_dict = property(lambda self: self.model.files_dict)
    fst_cache = property(lambda self: self.model.fst_cache)

    num_kaldi_rules = property(lambda self: self._num_kaldi_rules)
    lexicon_words = property(lambda self: self.model.lexicon_words)
    _longest_word = property(lambda self: self.model.longest_word)

    default_dictation_g_filepath = property(lambda self: os.path.join(self.model_dir, 'G_dictation.fst'))
    _dictation_fst_filepath = property(lambda self: os.path.join(self.model_dir, 'Dictation.fst'))

    @lazy_readonly_property
    def nonterm_phones_offset(self):
        offset = symbol_table_lookup(self.files_dict['phones.txt'], '#nonterm_bos')
        if offset is None:
            raise KaldiError("cannot find #nonterm_bos symbol in phones.txt")
        return offset

    def alloc_rule_id(self):
        id = self._num_kaldi_rules
        self._num_kaldi_rules += 1
        return id

    def free_rule_id(self):
        id = self._num_kaldi_rules
        self._num_kaldi_rules -= 1
        return id

    ####################################################################################################################
    # Methods for compiling graphs.

    def _compile_otf_graph(self, **kwargs):
        # FIXME: documentation
        with debug_timer(_log.debug, "otf graph compilation"):
            format_kwargs = dict(self.files_dict, **kwargs)
            run = lambda cmd, **kwargs: run_subprocess(cmd, format_kwargs, "otf graph compilation step", **kwargs)

            p1 = run("{exec_dir}fstcompile --isymbols={words_txt} --osymbols={words_txt} {filename}.txt {filename}")
            p2 = run("{exec_dir}fstrelabel --relabel_ipairs={g.irelabel} {filename} {filename}")
            p3 = run("{exec_dir}fstarcsort {filename} {filename}")
            # p4 = run("{exec_dir}fstconvert --fst_type=const {filename} {filename}")

    def _compile_agf_graph(self, compile=False, nonterm=False, input_data=None, input_filename=None, filename=None, **kwargs):
        """
        :param compile: bool whether to compile FST (False if it has already been compiled, like importing dictation FST)
        :param nonterm: bool whether rule represents a nonterminal in the active-grammar-fst (only False for the top FST?)
        """
        # Possible combinations of (compile,nonterm): (True,True) (True,False) (False,True)
        # FIXME: documentation
        with debug_timer(_log.debug, "agf graph compilation") as get_time_spent:
            verbose_level = 5 if _log.isEnabledFor(5) else 0
            format_kwargs = dict(self.files_dict, input_filename=input_filename, filename=filename, verbose=verbose_level, **kwargs)
            format_kwargs.update(nonterm_phones_offset=self.nonterm_phones_offset)

            if 1:
                # Pipeline-style
                if input_data and input_filename: raise KaldiError("_compile_agf_graph passed both input_data and input_filename")
                elif input_data: input = ExternalProcess.shell.echo(input_data)
                elif input_filename: input = input_filename
                else: raise KaldiError("_compile_agf_graph passed neither input_data nor input_filename")
                compile_command = input
                format = ExternalProcess.get_formatter(format_kwargs)
                args = []

                # if True: (input | ExternalProcess.fstcompile(*format('--isymbols={words_txt}', '--osymbols={words_txt}')) | ExternalProcess.fstinfo | 'stats.log+')()
                # if True: (ExternalProcess.shell.echo(input_data) | ExternalProcess.fstcompile(*format('--isymbols={words_txt}', '--osymbols={words_txt}')) | (filename+'-G'))()

                if compile:
                    compile_command |= ExternalProcess.fstcompile(*format('--isymbols={words_txt}', '--osymbols={words_txt}'))
                    args.extend(['--arcsort-grammar'])
                if nonterm:
                    args.extend(format('--grammar-prepend-nonterm={tmp_dir}nonterm_begin.fst'))
                    args.extend(format('--grammar-append-nonterm={tmp_dir}nonterm_end.fst'))
                args.extend(format('--nonterm-phones-offset={nonterm_phones_offset}', '--read-disambig-syms={disambig_int}', '--verbose={verbose}',
                    '{tree}', '{final_mdl}', '{L_disambig_fst}', '-', '{filename}'))
                kwargs = dict() if _log.isEnabledFor(logging.DEBUG) else dict(stderr=StringIO())
                compile_command |= ExternalProcess.compile_graph_agf(*args, **kwargs)
                # compile_command |= ExternalProcess.compile_graph_agf_debug(*args, **kwargs)
                # if len(input_data) >= 1000000:
                #     compile_command |= ExternalProcess.compile_graph_agf_debug(*args, **kwargs)
                # else:
                #     compile_command |= ExternalProcess.compile_graph_agf(*args, **kwargs)
                compile_command()

                # if True: (ExternalProcess.shell.echo('%s -> %s\n' % (len(input_data), get_time_spent())) | ExternalProcess.shell('cat') | 'stats.log+')()

            else:
                # CLI-style
                run = lambda cmd, **kwargs: run_subprocess(cmd, format_kwargs, "agf graph compilation step", format_kwargs_update=dict(input_filename=filename), **kwargs)
                if compile: run("{exec_dir}fstcompile --isymbols={words_txt} --osymbols={words_txt} {input_filename}.txt {filename}")
                # run("cp {input_filename} {filename}-G")
                if compile: run("{exec_dir}fstarcsort --sort_type=ilabel {input_filename} {filename}")
                if nonterm: run("{exec_dir}fstconcat {tmp_dir}nonterm_begin.fst {input_filename} {filename}")
                if nonterm: run("{exec_dir}fstconcat {input_filename} {tmp_dir}nonterm_end.fst {filename}")
                # run("cp {input_filename} {filename}-G")
                run("{exec_dir}compile-graph --nonterm-phones-offset={nonterm_phones_offset} --read-disambig-syms={disambig_int} --verbose={verbose}"
                    + " {tree} {final_mdl} {L_disambig_fst} {input_filename} {filename}")

    def _compile_base_fsts(self):
        filepaths = [self.tmp_dir + filename for filename in ['nonterm_begin.fst', 'nonterm_end.fst']]
        if all(self.fst_cache.is_current(filepath) for filepath in filepaths):
            return

        format_kwargs = dict(self.files_dict)
        def run(cmd): subprocess.check_call(cmd.format(**format_kwargs), shell=True)  # FIXME: unsafe shell?
        if platform == 'windows':
            run("(echo 0 1 #nonterm_begin 0^& echo 1) | {exec_dir}fstcompile.exe --isymbols={words_txt} > {tmp_dir}nonterm_begin.fst")
            run("(echo 0 1 #nonterm_end 0^& echo 1) | {exec_dir}fstcompile.exe --isymbols={words_txt} > {tmp_dir}nonterm_end.fst")
        else:
            run("(echo 0 1 \\#nonterm_begin 0; echo 1) | {exec_dir}fstcompile --isymbols={words_txt} > {tmp_dir}nonterm_begin.fst")
            run("(echo 0 1 \\#nonterm_end 0; echo 1) | {exec_dir}fstcompile --isymbols={words_txt} > {tmp_dir}nonterm_end.fst")

        for filepath in filepaths:
            self.fst_cache.add(filepath)

    def compile_top_fst(self):
        kaldi_rule = KaldiRule(self, 'top', nonterm=False)
        fst = kaldi_rule.fst
        state_initial = fst.add_state(initial=True)
        state_final = fst.add_state(final=True)
        for i in range(self._max_rule_id + 1):
            # fst.add_arc(state_initial, state_final, '#nonterm:rule'+str(i), olabel=WFST.eps)
            fst.add_arc(state_initial, state_final, '#nonterm:rule'+str(i), olabel='#nonterm:rule'+str(i))
        fst.equalize_weights()
        kaldi_rule.compile_file()
        return kaldi_rule

    def _get_dictation_fst_filepath(self):
        if os.path.exists(self._dictation_fst_filepath):
            return self._dictation_fst_filepath
        _log.error("cannot find dictation fst: %s", self._dictation_fst_filepath)
        # _log.error("using universal dictation fst")
    dictation_fst_filepath = property(_get_dictation_fst_filepath)

    # def _construct_dictation_states(self, fst, src_state, dst_state, number=(1,None), words=None, start_weight=None):
    #     """
    #     Matches `number` words.
    #     :param number: (0,None) or (1,None) or (1,1), where None is infinity.
    #     """
    #     # unweighted=0.01
    #     if words is None: words = self._lexicon_words
    #     word_probs = self._lexicon_word_probs
    #     backoff_state = fst.add_state()
    #     fst.add_arc(src_state, backoff_state, None, weight=start_weight)
    #     if number[0] == 0:
    #         fst.add_arc(backoff_state, dst_state, None)
    #     for word, prob in word_probs.items():
    #         state = fst.add_state()
    #         fst.add_arc(backoff_state, state, word, weight=prob)
    #         if number[1] == None:
    #             fst.add_arc(state, backoff_state, None)
    #         fst.add_arc(state, dst_state, None)

    def compile_universal_grammar(self, words=None):
        """recognizes any sequence of words"""
        kaldi_rule = KaldiRule(self, 'universal', nonterm=False)
        if words is None: words = self._lexicon_words
        fst = kaldi_rule.fst
        backoff_state = fst.add_state(initial=True, final=True)
        for word in words:
            # state = fst.add_state()
            # fst.add_arc(backoff_state, state, word)
            # fst.add_arc(state, backoff_state, None)
            fst.add_arc(backoff_state, backoff_state, word)
        kaldi_rule.compile_file()
        return kaldi_rule

    def compile_dictation_fst(self, g_filename):
        self._compile_agf_graph(input_filename=g_filename, filename=self._dictation_fst_filepath, nonterm=True)

    ####################################################################################################################
    # Methods for recognition.

    def prepare_for_recognition(self):
        self.fst_cache.save()

    def parse_output_for_rule(self, kaldi_rule, output):
        """Can be used even when self.parsing_framework == 'token', only for mimic (which contains no nonterms)."""
        try:
            parse_results = kaldi_rule.matcher.parseString(output, parseAll=True)
        except pp.ParseException:
            return None
        parsed_output = ' '.join(parse_results)
        if parsed_output.lower() != output:
            self._log.error("parsed_output(%r).lower() != output(%r)" % (parse_results, output))
        kaldi_rule_name = str(parse_results.getName())
        assert kaldi_rule_name == kaldi_rule.name
        words = parsed_output.split()
        return words

    cloud_dictation_regex = re.compile(r'(?<=#nonterm:dictation_cloud )(.*?)(?= #nonterm:end)')  # lookbehind & lookahead assertions

    def parse_output(self, output, dictation_info_func=None):
        assert self.parsing_framework == 'token'
        self._log.debug("parse_output(%r)" % output)
        if output == '':
            return None, [], []

        nonterm_token, _, parsed_output = output.partition(' ')
        assert nonterm_token.startswith('#nonterm:rule')
        kaldi_rule_id = int(nonterm_token[len('#nonterm:rule'):])
        kaldi_rule = self.kaldi_rule_by_id_dict[kaldi_rule_id]

        if self.cloud_dictation and dictation_info_func and kaldi_rule.has_dictation and '#nonterm:dictation_cloud' in parsed_output:
            try:
                audio_data, word_align = dictation_info_func()
                words, times, lengths = zip(*word_align)
                # Find start & end word-index & byte-offset of each cloud dictation span
                dictation_spans = [{
                        'index_start': index,
                        'offset_start': time,
                        'index_end': words.index('#nonterm:end', index),
                        'offset_end': times[words.index('#nonterm:end', index)],
                    }
                    for index, (word, time, length) in zip(range(len(word_align)), word_align)
                    if word.startswith('#nonterm:dictation_cloud')]

                # If last dictation is at end of utterance, include rest of audio_data; else, include half of audio_data between dictation end and start of next word
                dictation_span = dictation_spans[-1]
                if dictation_span['index_end'] == len(word_align) - 1:
                    dictation_span['offset_end'] = len(audio_data)
                else:
                    next_word_time = times[dictation_span['index_end'] + 1]
                    dictation_span['offset_end'] = (dictation_span['offset_end'] + next_word_time) / 2

                def replace_dictation(matchobj):
                    orig_text = matchobj.group(1)
                    dictation_span = dictation_spans.pop(0)
                    dictation_audio = audio_data[dictation_span['offset_start'] : dictation_span['offset_end']]
                    with debug_timer(self._log.debug, 'cloud dictation call'):
                        cloud_text = cloud.GCloud.transcribe_data_sync(dictation_audio)
                        self._log.debug("cloud_dictation: %.2fs audio -> %r", (0.5 * len(dictation_audio) / 16000), cloud_text)
                    # with debug_timer(self._log.debug, 'cloud dictation call'):
                    #     cloud_text = cloud.GCloud.transcribe_data_sync(dictation_audio, model='command_and_search')
                    #     self._log.debug("cloud_dictation: %.2fs audio -> %r", (0.5 * len(dictation_audio) / 16000), cloud_text)
                    # with debug_timer(self._log.debug, 'cloud dictation call'):
                    #     cloud_text = cloud.GCloud.transcribe_data_streaming(dictation_audio)
                    #     self._log.debug("cloud_dictation: %.2fs audio -> %r", (0.5 * len(dictation_audio) / 16000), cloud_text)
                    # cloud.write_wav('test.wav', dictation_audio)
                    return (cloud_text or orig_text)

                parsed_output = self.cloud_dictation_regex.sub(replace_dictation, parsed_output)
            except Exception as e:
                self._log.exception("Exception performing cloud dictation")

        words = []
        words_are_dictation = []
        in_dictation = False
        for word in parsed_output.split():
            if word.startswith('#nonterm:'):
                if word.startswith('#nonterm:dictation'):
                    in_dictation = True
                elif in_dictation and word == '#nonterm:end':
                    in_dictation = False
            else:
                words.append(word)
                words_are_dictation.append(in_dictation)

        # parsed_output = remove_nonterms(parsed_output)

        return kaldi_rule, words, words_are_dictation

########################################################################################################################
# Utility functions.

def remove_nonterms(text):
    return ' '.join(word for word in text.split() if not word.startswith('#nonterm:'))
