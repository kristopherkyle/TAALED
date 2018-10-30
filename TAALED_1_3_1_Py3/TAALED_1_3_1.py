#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.font
import tkinter.filedialog
import tkinter.constants
import queue
from tkinter import messagebox
import os
import sys
import re
import platform
import glob
import math
from collections import Counter
from threading import Thread

#This creates a que in which the core TAALED program can communicate with the GUI
dataQueue = queue.Queue()

#This creates the message for the progress box (and puts it in the dataQueue)
progress = "...Waiting for Data to Process"
dataQueue.put(progress)

#Def1 is the core TAALED program; args is information passed to TAALED
def start_thread(def1, arg1, arg2, arg3): 
	t = Thread(target=def1, args=(arg1, arg2, arg3))
	t.start()

#This allows for a packaged gui to find the resource files.
def resource_path(relative):
	if hasattr(sys, "_MEIPASS"):
		return os.path.join(sys._MEIPASS, relative)
	return os.path.join(relative)

color = "#758fa8"

prog_name = "TAALED 1.3.1"

if platform.system() == "Darwin":
	system = "M"
	title_size = 16
	font_size = 14
	geom_size = "525x500"
elif platform.system() == "Windows":
	system = "W"
	title_size = 12
	font_size = 12
	geom_size = "525x475"
elif platform.system() == "Linux":
	system = "L"
	title_size = 14
	font_size = 12
	geom_size = "525x385"

def start_watcher(def2, count, folder):
	t2 = Thread(target=def2, args =(count,folder))
	t2.start()

class MyApp: #this is the class for the gui and the text analysis
	def __init__(self, parent):
				
		helv14= tkinter.font.Font(family= "Helvetica Neue", size=font_size)
		times14= tkinter.font.Font(family= "Lucida Grande", size=font_size)
		helv16= tkinter.font.Font(family= "Helvetica Neue", size = title_size, weight = "bold", slant = "italic")

				#This defines the GUI parent (ish)
		
		self.myParent = parent
		
		self.var_dict = {}
		
		#This creates the header text - Task:work with this to make more pretty!
		self.spacer1= tk.Label(parent, text= "Tool for the Automatic Analysis of Lexical Diversity", font = helv16, background = color)
		self.spacer1.pack()
		
		#This creates a frame for the meat of the GUI
		self.thestuff= tk.Frame(parent, background =color)
		self.thestuff.pack()
		
		self.myContainer1= tk.Frame(self.thestuff, background = color)
		self.myContainer1.pack(side = tk.RIGHT, expand= tk.TRUE)
		self.instruct = tk.Button(self.myContainer1, text = "Instructions", justify = tk.LEFT)
		self.instruct.pack()
		self.instruct.bind("<Button-1>", self.instruct_mess)
		
		self.opt_frame = tk.LabelFrame(self.myContainer1, text= "Options and index selection", background = color)
		self.opt_frame.pack(fill = tk.X,expand=tk.TRUE)
		
		self.options_frame = tk.LabelFrame(self.opt_frame, text= "Word analysis options", background = color)
		self.options_frame.pack(fill = tk.X,expand=tk.TRUE)
		
		#insert checkboxes here
		self.aw_choice_var = tk.IntVar()
		self.aw_choice = tk.Checkbutton(self.options_frame, text="All words", variable=self.aw_choice_var,background = color)
		self.aw_choice.grid(row=1,column=1, sticky = "W")	
		self.var_dict["aw"] = self.aw_choice_var
		
		self.cw_choice_var = tk.IntVar()
		self.cw_choice = tk.Checkbutton(self.options_frame, text="Content words", variable=self.cw_choice_var,background = color)
		self.cw_choice.grid(row=1,column=2, sticky = "W")	
		self.var_dict["cw"] = self.cw_choice_var

		self.fw_choice_var = tk.IntVar()
		self.fw_choice = tk.Checkbutton(self.options_frame, text="Function words", variable=self.fw_choice_var,background = color)
		self.fw_choice.grid(row=1,column=3, sticky = "W")	
		self.var_dict["fw"] = self.fw_choice_var

		self.indices_frame = tk.LabelFrame(self.opt_frame, text= "Index selection", background = color)
		self.indices_frame.pack(fill = tk.X,expand=tk.TRUE)

		self.simple_ttr_var = tk.IntVar()
		self.simple_ttr = tk.Checkbutton(self.indices_frame, text="Simple TTR", variable=self.simple_ttr_var,background = color)
		self.simple_ttr.grid(row=1,column=1, sticky = "W")
		self.var_dict["simple_ttr"] = self.simple_ttr_var
		
		self.root_ttr_var = tk.IntVar()
		self.root_ttr = tk.Checkbutton(self.indices_frame, text="Root TTR", variable=self.root_ttr_var,background = color)
		self.root_ttr.grid(row=1,column=2, sticky = "W")
		self.var_dict["root_ttr"] = self.root_ttr_var

		self.bi_log_ttr_var = tk.IntVar()
		self.bi_log_ttr = tk.Checkbutton(self.indices_frame, text="Log TTR", variable=self.bi_log_ttr_var,background = color)
		self.bi_log_ttr.grid(row=1,column=3, sticky = "W")
		self.var_dict["log_ttr"] = self.bi_log_ttr_var

		self.maas_ttr_var = tk.IntVar()
		self.maas_ttr = tk.Checkbutton(self.indices_frame, text="Maas", variable=self.maas_ttr_var,background = color)
		self.maas_ttr.grid(row=1,column=4, sticky = "W")
		self.var_dict["maas_ttr"] = self.maas_ttr_var

		self.mattr_var = tk.IntVar()
		self.mattr = tk.Checkbutton(self.indices_frame, text="MATTR", variable=self.mattr_var,background = color)
		self.mattr.grid(row=2,column=1, sticky = "W")
		self.var_dict["mattr"] = self.mattr_var

		self.msttr_var = tk.IntVar()
		self.msttr = tk.Checkbutton(self.indices_frame, text="MSTTR", variable=self.msttr_var,background = color)
		self.msttr.grid(row=2,column=2, sticky = "W")
		self.var_dict["msttr"] = self.msttr_var
		
		self.hdd_var = tk.IntVar()
		self.hdd = tk.Checkbutton(self.indices_frame, text="HD-D", variable=self.hdd_var,background = color)
		self.hdd.grid(row=2,column=3, sticky = "W")
		self.var_dict["hdd"] = self.hdd_var
		
		self.mtld_orig_var = tk.IntVar()
		self.mtld_orig = tk.Checkbutton(self.indices_frame, text="MTLD Original", variable=self.mtld_orig_var,background = color)
		self.mtld_orig.grid(row=3,column=1, sticky = "W")
		self.var_dict["mltd"] = self.mtld_orig_var
		
		self.mltd_ma_var = tk.IntVar()
		self.mltd_ma = tk.Checkbutton(self.indices_frame, text="MTLD MA Bi", variable=self.mltd_ma_var,background = color)
		self.mltd_ma.grid(row=3,column=2, sticky = "W")
		self.var_dict["mltd_ma"] = self.mltd_ma_var

		self.mltd_wrap_var = tk.IntVar()
		self.mltd_wrap = tk.Checkbutton(self.indices_frame, text="MTLD MA Wrap", variable=self.mltd_wrap_var,background = color)
		self.mltd_wrap.grid(row=3,column=3, sticky = "W")
		self.var_dict["mtld_wrap"] = self.mltd_wrap_var

		self.secondframe= tk.LabelFrame(self.myContainer1, text= "Data input", background = color)
		self.secondframe.pack(fill = tk.X,expand=tk.TRUE) 
		
		
		#Creates default dirname so if statement in Process Texts can check to see
		#if a directory name has been chosen
		self.dirname = ""
		
		#This creates a label for the first program input (Input Directory)
		self.inputdirlabel =tk.LabelFrame(self.secondframe, height = "1", width= "45", padx = "4", text = "Your selected input folder:", background = color)
		self.inputdirlabel.pack(fill = tk.X)
		
		#Creates label that informs user which directory has been chosen
		directoryprompt = "(No Folder Chosen)"
		self.inputdirchosen = tk.Label(self.inputdirlabel, height= "1", width= "45", justify=tk.LEFT, padx = "4", anchor = tk.W, font= helv14, text = directoryprompt)
		self.inputdirchosen.pack(side = tk.LEFT)
		
		#This Places the first button under the instructions.
		self.button1 = tk.Button(self.inputdirlabel)
		self.button1.configure(text= "Select")
		self.button1.pack(side = tk.LEFT, padx = 5)
		
		self.button1.bind("<Button-1>", self.button1Click)
		
		self.outdirname = ""
	
		self.out_optframe = tk.LabelFrame(self.secondframe, height = "1", width= "45", padx = "4", text = "Output Options", background = color)
		self.out_optframe.pack()
		
		self.ind_out_var = tk.IntVar()
		self.ind_out = tk.Checkbutton(self.out_optframe, text="Individual Item Output", variable=self.ind_out_var,background = color)
		self.ind_out.pack(side = tk.LEFT)	
		self.ind_out.deselect()
		self.var_dict["indout"] = self.ind_out_var
										
		#Creates a label for the second program input (Output Directory)
		self.outputdirlabel = tk.LabelFrame(self.secondframe, height = "1", width= "45", padx = "4", text = "Your selected output filename:", background = color)
		self.outputdirlabel.pack(fill = tk.X)
				
		#Creates a label that informs sure which directory has been chosen
		outdirectoryprompt = "(No Output Filename Chosen)"
		self.outputdirchosen = tk.Label(self.outputdirlabel, height= "1", width= "45", justify=tk.LEFT, padx = "4", anchor = tk.W, font= helv14, text = outdirectoryprompt)
		self.outputdirchosen.pack(side = tk.LEFT)
		
		self.button2 = tk.Button(self.outputdirlabel)
		self.button2["text"]= "Select"
		#This tells the button what to do if clicked.
		self.button2.bind("<Button-1>", self.button2Click)
		self.button2.pack(side = tk.LEFT, padx = 5)

		self.BottomSpace= tk.LabelFrame(self.myContainer1, text = "Run Program", background = color)
		self.BottomSpace.pack()

		self.button3= tk.Button(self.BottomSpace)
		self.button3["text"] = "Process Texts"
		self.button3.bind("<Button-1>", self.runprogram)
		self.button3.pack()

		self.progresslabelframe = tk.LabelFrame(self.BottomSpace, text= "Program Status", background = color)
		self.progresslabelframe.pack(expand= tk.TRUE)
		
		self.progress= tk.Label(self.progresslabelframe, height= "1", width= "45", justify=tk.LEFT, padx = "4", anchor = tk.W, font= helv14, text=progress)
		self.progress.pack()
		
		self.poll(self.progress)
	
	def poll(self, function):
		
		self.myParent.after(10, self.poll, function)
		try:
			function.config(text = dataQueue.get(block=False))
			
		except queue.Empty:
			pass
	
	def instruct_mess(self, event):
		messagebox.showinfo("Instructions", "1. Click the 'Index Selection and Options' button to select desired indices\n\n2. Choose the input folder (where your files are)\n\n3. If desired, select additional output options (see user manual for details)\n\n4. Choose your output filename\n\n5. Press the 'Process Texts' button")

	def entry1Return(self,event):
		input= self.entry1.get()
		self.input2 = input + ".csv"
		self.filechosenchosen.config(text = self.input2)
		self.filechosenchosen.update_idletasks()
		
	#Following is an example of how we can update the information from users...
	def button1Click(self, event):
		#import Tkinter, 
		if sys.version_info[0] == 2: 
			import tkFileDialog
			self.dirname = tkFileDialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')

		if sys.version_info[0] == 3:
			import tkinter.filedialog
			self.dirname = tkinter.filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
		
		self.displayinputtext = '.../'+self.dirname.split('/')[-1]
		self.inputdirchosen.config(text = self.displayinputtext)
		

	def button2Click(self, event):
		self.outdirname = tkinter.filedialog.asksaveasfilename(parent=root, defaultextension = ".csv", initialfile = "results",title='Choose Output Filename')
		
		#print(self.outdirname)
		if self.outdirname == "":
			self.displayoutputtext = "(No Output Filename Chosen)"
		else: self.displayoutputtext = '.../' + self.outdirname.split('/')[-1]
		self.outputdirchosen.config(text = self.displayoutputtext)

	def runprogram(self, event):
		self.poll(self.progress)
		start_thread(main, self.dirname, self.outdirname, self.var_dict)

		
#### THIS IS BEGINNING OF PROGRAM ###			
def main(indir, outdir, var_dict):
	
	import tkinter.messagebox
	if indir is "":
		tkinter.messagebox.showinfo("Supply Information", "Choose Input Directory")
	if outdir is "":
		tkinter.messagebox.showinfo("Choose Output Directory", "Choose Output Directory")

	
	if indir is not "" and outdir is not "":
		dataQueue.put("Starting TAALED...")
	
	import spacy
	from spacy.util import set_data_path
	set_data_path(resource_path('dep_files/en_core_web_sm'))
	nlp = spacy.load(resource_path('dep_files/en_core_web_sm'))
	
	#thus begins the text analysis portion of the program
	adj_word_list = open(resource_path("dep_files/adj_lem_list.txt"), "r",errors = 'ignore').read().split("\n")[:-1]
	real_word_list = open(resource_path("dep_files/real_words.txt"), "r",errors = 'ignore').read().split("\n")[:-1]
	
	### THESE ARE PERTINENT FOR ALL IMPORTANT INDICES ####
	noun_tags = ["NN", "NNS", "NNP", "NNPS"] #consider whether to identify gerunds
	proper_n = ["NNP", "NNPS"]
	no_proper = ["NN", "NNS"]
	pronouns = ["PRP", "PRP$"]
	adjectives = ["JJ", "JJR", "JJS"]
	verbs = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "MD"]
	adverbs = ["RB", "RBR", "RBS"]
	content = ["NN", "NNS", "NNP", "NNPS","JJ", "JJR", "JJS"] #note that this is a preliminary list
	prelim_not_function = ["NN", "NNS", "NNP", "NNPS","JJ", "JJR", "JJS", "RB", "RBR", "RBS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "MD"]
	pronoun_dict = {"me":"i","him":"he","her":"she"}
	punctuation = "`` '' ' . , ? ! ) ( % / - _ -LRB- -RRB- SYM : ;".split(" ")
	punctuation.append('"')

	#This function deals with denominator issues that can kill the program:
	def safe_divide(numerator, denominator):
		if denominator == 0 or denominator == 0.0:
			index = 0
		else: index = numerator/denominator
		return index
	
	def indexer(header_list, index_list, name, index):
		header_list.append(name)
		index_list.append(index)

	def tag_processor_spaCy(raw_text): #uses default spaCy 2.016
		
		lemma_list = []
		content_list = []
		function_list = []

		tagged_text = nlp(raw_text)
		
		for sent in tagged_text.sents:
			for token in sent:			
				if token.tag_ in punctuation:
					continue
				if token.text not in real_word_list:
					continue
			
			
				if token.tag_ in content:
					if token.tag_ in noun_tags:
						content_list.append(token.lemma_ + "_cw_nn")
						lemma_list.append(token.lemma_ + "_cw_nn")
					else:
						content_list.append(token.lemma_ + "_cw")
						lemma_list.append(token.lemma_ + "_cw")
			
				if token.tag_ not in prelim_not_function:
					if token.tag_ in pronouns:
						if token.text.lower() in pronoun_dict:
							function_list.append(pronoun_dict[token.text.lower()] + "_fw")
							lemma_list.append(pronoun_dict[token.text.lower()] + "_fw")
						else:
							function_list.append(token.text.lower() + "_fw")
							lemma_list.append(token.text.lower() + "_fw")
					else:
						function_list.append(token.lemma_ + "_fw")
						lemma_list.append(token.lemma_ + "_fw")
				
				if token.tag_ in verbs:						
					if token.dep_ == "aux":
						function_list.append(token.lemma_ + "_fw")
						lemma_list.append(token.lemma_ + "_fw")
					
					elif token.lemma_ == "be":
						function_list.append(token.lemma_ + "_fw")
						lemma_list.append(token.lemma_ + "_fw")

					else:
						content_list.append(token.lemma_ + "_cw_vb")
						lemma_list.append(token.lemma_ + "_cw_vb")				
			
				if token.tag_ in adverbs:
					if (token.lemma_[-2:] == "ly" and token.lemma_[:-2] in adj_word_list) or (token.lemma_[-4:] == "ally" and token.lemma_[:-4] in adj_word_list):
						content_list.append(token.lemma_ + "_cw")
						lemma_list.append(token.lemma_ + "_cw")				
					else:
						function_list.append(token.lemma_ + "_fw")
						lemma_list.append(token.lemma_ + "_fw")				
				#print(raw_token, lemma_list[-1])
					
		return {"lemma" : lemma_list, "content" : content_list, "function":function_list}
				
	def lex_density(cw_text, fw_text):
			n_cw = len(cw_text)
			n_fw = len(fw_text)
			n_all = n_cw + n_fw
	
			n_type_cw = len(set(cw_text))
			n_type_fw = len(set(fw_text))
			n_all_type = n_type_cw + n_type_fw
	
			lex_dens_all = safe_divide(n_cw,n_all) #percentage of content words
			lex_dens_cw_fw = safe_divide(n_cw,n_fw) #ratio content words to function words
	
			lex_dens_all_type = safe_divide(n_type_cw,n_all_type) #percentage of content words
			lex_dens_cw_fw_type = safe_divide(n_type_cw,n_type_fw) #ratio content words to function words
			
			return [lex_dens_all, lex_dens_all_type]
			
	def ttr(text):
		ntokens = len(text)
		ntypes = len(set(text))

		simple_ttr = safe_divide(ntypes,ntokens)
		root_ttr = safe_divide(ntypes, math.sqrt(ntokens))
		log_ttr = safe_divide(math.log10(ntypes), math.log10(ntokens))
		maas_ttr = safe_divide((math.log10(ntokens)-math.log10(ntypes)), math.pow(math.log10(ntokens),2))

		return [simple_ttr,root_ttr,log_ttr,maas_ttr]

	def simple_ttr(text):
		ntokens = len(text)
		ntypes = len(set(text))
		
		return safe_divide(ntypes,ntokens)

	def root_ttr(text):
		ntokens = len(text)
		ntypes = len(set(text))
		
		return safe_divide(ntypes, math.sqrt(ntokens))

	def log_ttr(text):
		ntokens = len(text)
		ntypes = len(set(text))
		
		return safe_divide(math.log10(ntypes), math.log10(ntokens))

	def maas_ttr(text):
		ntokens = len(text)
		ntypes = len(set(text))
		
		return safe_divide((math.log10(ntokens)-math.log10(ntypes)), math.pow(math.log10(ntokens),2))


	def mattr(text, window_length = 50): #from TAACO 2.0.4

		if len(text) < (window_length + 1):
			ma_ttr = safe_divide(len(set(text)),len(text))

		else:
			sum_ttr = 0
			denom = 0
			for x in range(len(text)):
				small_text = text[x:(x + window_length)]
				if len(small_text) < window_length:
					break
				denom += 1
				sum_ttr+= safe_divide(len(set(small_text)),float(window_length)) 
			ma_ttr = safe_divide(sum_ttr,denom)
	
		return ma_ttr

	def msttr(text, window_length = 50):

		if len(text) < (window_length + 1):
			ms_ttr = safe_divide(len(set(text)),len(text))

		else:
			sum_ttr = 0
			denom = 0

			n_segments = int(safe_divide(len(text),window_length))
			seed = 0
			for x in range(n_segments):
				sub_text = text[seed:seed+window_length]
				#print sub_text
				sum_ttr += safe_divide(len(set(sub_text)), len(sub_text))
				denom+=1
				seed+=window_length

			ms_ttr = safe_divide(sum_ttr, denom)

		return ms_ttr

	def hdd(text):
		#requires Counter import
		def choose(n, k): #calculate binomial
			"""
			A fast way to calculate binomial coefficients by Andrew Dalke (contrib).
			"""
			if 0 <= k <= n:
				ntok = 1
				ktok = 1
				for t in range(1, min(k, n - k) + 1): #this was changed to "range" from "xrange" for py3
					ntok *= n
					ktok *= t
					n -= 1
				return ntok // ktok
			else:
				return 0
	
		def hyper(successes, sample_size, population_size, freq): #calculate hypergeometric distribution
			#probability a word will occur at least once in a sample of a particular size
			try:
				prob_1 = 1.0 - (float((choose(freq, successes) * choose((population_size - freq),(sample_size - successes)))) / float(choose(population_size, sample_size)))
				prob_1 = prob_1 * (1/sample_size)
			except ZeroDivisionError:
				prob_1 = 0
				
			return prob_1

		prob_sum = 0.0
		ntokens = len(text)
		types_list = list(set(text))
		frequency_dict = Counter(text)

		for items in types_list:
			prob = hyper(0,42,ntokens,frequency_dict[items]) #random sample is 42 items in length
			prob_sum += prob

		return prob_sum 


	def mtld_original(input, min = 10):
		def mtlder(text):
			factor = 0
			factor_lengths = 0
			start = 0
			for x in range(len(text)):
				factor_text = text[start:x+1]
				if x+1 == len(text):
					factor += safe_divide((1 - ttr(factor_text)[0]),(1 - .72))
					factor_lengths += len(factor_text)
				else:
					if ttr(factor_text)[0] < .720 and len(factor_text) >= min:
						factor += 1
						factor_lengths += len(factor_text)
						start = x+1
					else:
						continue

			mtld = safe_divide(factor_lengths,factor)
			return mtld
		input_reversed = list(reversed(input))
		mtld_full = safe_divide((mtlder(input)+mtlder(input_reversed)),2)
		return mtld_full

	def mtld_bi_directional_ma(text, min = 10):
		def mtld_ma(text, min = 10):
			factor = 0
			factor_lengths = 0
			for x in range(len(text)):
				sub_text = text[x:]
				breaker = 0
				for y in range(len(sub_text)):
					if breaker == 0:
						factor_text = sub_text[:y+1]	
						if ttr(factor_text)[0] < .720 and len(factor_text) >= min:
							factor += 1
							factor_lengths += len(factor_text)
							breaker = 1
						else:
							continue
			mtld = safe_divide(factor_lengths,factor)
			return mtld

		forward = mtld_ma(text)
		backward = mtld_ma(list(reversed(text)))

		mtld_bi = safe_divide((forward + backward), 2) #average of forward and backward mtld

		return mtld_bi


	def mtld_ma_wrap(text, min = 10):
		factor = 0
		factor_lengths = 0
		start = 0
		double_text = text + text #allows wraparound
		for x in range(len(text)):
			breaker = 0
			sub_text = double_text[x:]
			for y in range(len(sub_text)):
				if breaker == 0:
					factor_text = sub_text[:y+1]
					if ttr(factor_text)[0] < .720 and len(factor_text) >= min:
						factor += 1
						factor_lengths += len(factor_text)
						breaker = 1
					else:
						continue
		mtld = safe_divide(factor_lengths,factor)
		return mtld


#### END DEFINED FUNCTIONS ####
	
	for keys in var_dict:
		try:
			if var_dict[keys].get() == 1:
				var_dict[keys] = 1
			else: var_dict[keys] = 0
		except AttributeError:
			continue
	
	inputfile = indir + "/*.txt"	
	outf=open(outdir, "w")
	
	filenames = glob.glob(inputfile)
	file_number = 0
	
	if var_dict["indout"] == 1:
		directory = outdir[:-4] + "_diagnostic/" #this is for diagnostic file
		if not os.path.exists(directory):
			os.makedirs(directory)
	
		for the_file in os.listdir(directory): #this cleans out the old diagnostic file (if applicable)
			file_path = os.path.join(directory, the_file)
			os.unlink(file_path)

	
	nfiles = len(filenames)
	file_counter = 1

	
	for filename in filenames:
		
		if system == "M" or system == "L":
			simple_filename = filename.split("/")[-1]
		
		if system == "W":
			simple_filename = filename.split("\\")[-1]
			if "/" in simple_filename:
				simple_filename = simple_filename.split("/")[-1]
		
		#print(simple_filename)
		
		if var_dict["indout"] == 1:
			basic_diag_file_name = directory + simple_filename[:-4] + "_processed.txt"
			basic_diag_file = open(basic_diag_file_name, "w")

		index_list = [simple_filename]
		header_list = ["filename"]
		
		#updates Program Status
		filename1 = ("Processing: " + str(file_counter) + " of " + str(nfiles) + " files")
		dataQueue.put(filename1)
		root.update_idletasks()
		
		file_counter+=1

		if system == "M" or system == "L":
			filename_2 = filename.split("/")[-1]
		elif system == "W":
			filename_2 = filename.split("\\")[-1]

		raw_text= open(filename, "r", errors = 'ignore').read()
		raw_text = re.sub('\s+',' ',raw_text)
		#while "	 " in raw_text:
			#raw_text = raw_text.replace("  ", " ")		
		
		refined_lemma_dict = tag_processor_spaCy(raw_text)
		
		lemma_text_aw = refined_lemma_dict["lemma"]
		
		lemma_text_cw = refined_lemma_dict["content"]
		lemma_text_fw = refined_lemma_dict["function"]
		
		indexer(header_list, index_list, "basic_ntokens",  len(lemma_text_aw))
		indexer(header_list, index_list, "basic_ntypes",  len(set(lemma_text_aw)))
		indexer(header_list, index_list, "basic_ncontent_tokens",  len(lemma_text_cw))
		indexer(header_list, index_list, "basic_ncontent_types",  len(set(lemma_text_cw)))
		indexer(header_list, index_list, "basic_nfunction_tokens",	len(lemma_text_fw))
		indexer(header_list, index_list, "basic_nfunction_types",  len(set(lemma_text_fw)))

		indexer(header_list, index_list, "lexical_density_types",  lex_density(lemma_text_cw, lemma_text_fw)[1])
		indexer(header_list, index_list, "lexical_density_tokens",	lex_density(lemma_text_cw, lemma_text_fw)[0])
	
		if var_dict["simple_ttr"] == 1:
			if var_dict["aw"] ==1:
				indexer(header_list, index_list, "simple_ttr_aw", ttr(lemma_text_aw)[0])
			
			if var_dict["cw"] ==1:
				indexer(header_list, index_list, "simple_ttr_cw", ttr(lemma_text_cw)[0])
			if var_dict["fw"] ==1:
				indexer(header_list, index_list, "simple_ttr_fw", ttr(lemma_text_fw)[0])
		
		if var_dict["root_ttr"] == 1:
			if var_dict["aw"] ==1:
				indexer(header_list, index_list, "root_ttr_aw", ttr(lemma_text_aw)[1])

			if var_dict["cw"] ==1:
				indexer(header_list, index_list, "root_ttr_cw", ttr(lemma_text_cw)[1])
			if var_dict["fw"] ==1:
				indexer(header_list, index_list, "root_ttr_fw", ttr(lemma_text_fw)[1])

		if var_dict["log_ttr"] == 1:
			if var_dict["aw"] ==1:
				indexer(header_list, index_list, "log_ttr_aw", ttr(lemma_text_aw)[2])

			if var_dict["cw"] ==1:
				indexer(header_list, index_list, "log_ttr_cw", ttr(lemma_text_cw)[2])
			if var_dict["fw"] ==1:
				indexer(header_list, index_list, "log_ttr_fw", ttr(lemma_text_fw)[2])

		if var_dict["maas_ttr"] == 1:
			if var_dict["aw"] ==1:
				indexer(header_list, index_list, "maas_ttr_aw", ttr(lemma_text_aw)[3])

			if var_dict["cw"] ==1:
				indexer(header_list, index_list, "maas_ttr_cw", ttr(lemma_text_cw)[3])
			if var_dict["fw"] ==1:
				indexer(header_list, index_list, "maas_ttr_fw", ttr(lemma_text_fw)[3])
		
		if var_dict["mattr"] == 1:
			if var_dict["aw"] ==1:
				indexer(header_list, index_list, "mattr50_aw", mattr(lemma_text_aw,50))

			if var_dict["cw"] ==1:
				indexer(header_list, index_list, "mattr50_cw", mattr(lemma_text_cw,50))
			if var_dict["fw"] ==1:
				indexer(header_list, index_list, "mattr50_fw", mattr(lemma_text_fw,50))

		if var_dict["msttr"] == 1:
			if var_dict["aw"] ==1:
				indexer(header_list, index_list, "msttr50_aw", msttr(lemma_text_aw,50))
			if var_dict["cw"] ==1:
				indexer(header_list, index_list, "msttr50_cw", msttr(lemma_text_cw,50))
			if var_dict["fw"] ==1:
				indexer(header_list, index_list, "msttr50_fw", msttr(lemma_text_fw,50))

		if var_dict["hdd"] == 1:
			if var_dict["aw"] ==1:
				indexer(header_list, index_list, "hdd42_aw", hdd(lemma_text_aw))

			if var_dict["cw"] ==1:
				indexer(header_list, index_list, "hdd42_cw", hdd(lemma_text_cw))
			if var_dict["fw"] ==1:
				indexer(header_list, index_list, "hdd42_fw", hdd(lemma_text_fw))

		if var_dict["mltd"] == 1:
			if var_dict["aw"] ==1:
				indexer(header_list, index_list, "mtld_original_aw", mtld_original(lemma_text_aw))

			if var_dict["cw"] ==1:
				indexer(header_list, index_list, "mtld_original_cw", mtld_original(lemma_text_cw))
			if var_dict["fw"] ==1:
				indexer(header_list, index_list, "mtld_original_fw", mtld_original(lemma_text_fw))

		if var_dict["mltd_ma"] == 1:
			if var_dict["aw"] ==1:
				indexer(header_list, index_list, "mtld_ma_bi_aw", mtld_bi_directional_ma(lemma_text_aw))

			if var_dict["cw"] ==1:
				indexer(header_list, index_list, "mtld_ma_bi_cw", mtld_bi_directional_ma(lemma_text_cw))
			if var_dict["fw"] ==1:
				indexer(header_list, index_list, "mtld_ma_bi_fw", mtld_bi_directional_ma(lemma_text_fw))

		if var_dict["mtld_wrap"] == 1:
			if var_dict["aw"] ==1:
				indexer(header_list, index_list, "mtld_ma_wrap_aw", mtld_ma_wrap(lemma_text_aw))

			if var_dict["cw"] ==1:
				indexer(header_list, index_list, "mtld_ma_wrap_cw", mtld_ma_wrap(lemma_text_cw))
			if var_dict["fw"] ==1:
				indexer(header_list, index_list, "mtld_ma_wrap_fw", mtld_ma_wrap(lemma_text_fw))

#### output for user ###		
		if var_dict["indout"] == 1:
			
			basic_diag_file.write("tokens\n\n")

			for diags in lemma_text_aw:
				try:
					basic_diag_file.write(diags+"\n")
				except UnicodeEncodeError:
					basic_diag_file.write("encoding error!\n")
			
			basic_diag_file.write("\ntypes\n\n")
			
			for diags in list(set(lemma_text_aw)):
				try:
					basic_diag_file.write(diags+"\n")
				except UnicodeEncodeError:
					basic_diag_file.write("encoding error!\n")
			
			basic_diag_file.flush()

### end output for user ###			

		if file_number == 0:
			header_out = ",".join(header_list) + "\n"
			outf.write(header_out)
			file_number +=1
		
		out_list = []
		for vars in index_list:
			out_list.append(str(vars))
		outstring = ",".join(out_list) + "\n"
		outf.write(outstring)

	
	nfiles = len(filenames)
	finishmessage = ("Processed " + str(nfiles) + " Files")
	dataQueue.put(finishmessage)
	if system == "M":
		messagebox.showinfo("Finished!", "TAALED has converted your files to numbers.\n\n Now the real work begins!")


if __name__ == '__main__':		
	root = tk.Tk()
	root.wm_title(prog_name)
	root.configure(background = color)
	root.geometry(geom_size)
	myapp = MyApp(root)
	root.mainloop()