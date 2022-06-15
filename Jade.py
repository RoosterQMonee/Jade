import sys

# --// Run

print("[ - Jade - ] - 1.1.2 - Universal")
print("[ - Devs - ] - Rooster, Mosvelt")

# --// Handle sys argv

verbose = False

compiler_args = ''.join(sys.argv)
if "-h" in compiler_args or "--help" in compiler_args:
	print("""
				[ - Jade - ] - 1.1.2 - Universal
				[ - Devs - ] - Rooster, Mosvelt

				-# Usage

				jade <FILENAME> [-h], [-v], [-c], [--help], [--verbose], [--credits]
				""")
	
	sys.exit()

if "-c" in compiler_args or "--credits" in compiler_args:
	print("""
				[ - Jade - ] - 1.1.2 -Universal
				[ - Devs - ] - Rooster, Mosvelt

				Programmer: Rooster
				Designer: Mosvelt
				""")
	
	sys.exit()
	
if "-v" in compiler_args or "--verbose" in compiler_args:
	verbose = True

# --// Variables

file = sys.argv[1]
arguments = ""

end_tokens = " ;\n"
str_tokens = "'\""
math_tokens = "+-/*^"
int_tokens = "1234567890"

num = 0
skip_index = 0
lskip_index = 0

func = False
args = False
loop = False
comment = False
used_num = False
used_token = False
used_variable = False

func_tokens = {}
loop_tokens = {}
variables = {}
if_cache = []
compiled = {}


if verbose == False:
	with open(file, "r") as jde:
		contents = jde.read()

		tokens = []
		
		token = ""
		string = ""
		integer = ""

		is_int = False
		is_str = False

	# --// Parse file contents
		
		for char in contents:

	# --// Get strings

			if char == "#":
				comment = True
			
			if char in str_tokens:
				if is_str == False:
					is_str = True

				elif is_str == True:
					is_str = False
					tokens.append(string)
					string = ""
					
					continue
			
				continue

			if char == "(" and is_str == False:
				if tokens != "":
					tokens.append(token)
					token = ""
				
				args = True
				arguments += char
				continue

			if char == ")" and is_str == False:
				args = False
				arguments += char

				tokens.append(arguments)
				arguments = ""
				
				continue

	# --// Check for a string

			if args == True:
				arguments += char
				continue
			
			if is_str == True:
				string += char
				continue

	# --// Check for arethmatic
			if char in int_tokens:
				if is_int == False:
					is_int = True

					integer += char

					continue

				integer += char
				token = ""

				continue

			if is_int == True:
				is_int = False
				tokens.append(integer)
				integer = ""
			
			if char in math_tokens:
				tokens.append(char)

				token = ""

				continue

	# --// Check for end line

			if comment == True:
				if char != "\n":
					continue

				else:
					comment = False
					continue
				
			if char in end_tokens:
				tokens.append(token)
				token = ""
				continue

	# --// Append to token
			
			token += char

	# --// Remove empty tokens

	for index, token in enumerate(tokens):
		if token == "" or token == "\n" or token == "":
			tokens.pop(index)

	# --// Show parsed tokens

	#print("Raw Parse: ", tokens)

	# --// Compile raw data

	def compile_arithmetic():
		global used_num
		global num
		global tokens

	# --// Parse
		
		for index, token in enumerate(tokens):
			
			if used_num == True:
				used_num = False
				continue

	# --// Check for arithmetic tokens
			
			if token in math_tokens:
				if token == "+":
					num = str(float(tokens[index-1])+float(tokens[index+1]))
					tokens[index] = num
					tokens.pop(index-1)
					tokens.pop(index)
					
					num = 0
					
					compile_arithmetic()
					break

	# --// Subtraction
				
				if token == "-":
					num = str(float(tokens[index-1])-float(tokens[index+1]))
					tokens[index] = num
					tokens.pop(index-1)
					tokens.pop(index)
					
					num = 0
					
					compile_arithmetic()
					break

	# --// Multiplication
				
				if token == "*":
					num = str(float(tokens[index-1])*float(tokens[index+1]))
					tokens[index] = num
					tokens.pop(index-1)
					tokens.pop(index)
					
					num = 0
					
					compile_arithmetic()
					break

	# --// Division
				
				if token == "/":
					num = str(float(tokens[index-1])/float(tokens[index+1]))
					tokens[index] = num
					tokens.pop(index-1)
					tokens.pop(index)
		
					num = 0

					compile_arithmetic()
					break

	# --// Exponenets
					
				if token == "^":
					num = str(float(tokens[index-1])^float(tokens[index+1]))
					tokens[index] = num
					tokens.pop(index-1)
					tokens.pop(index)
		
					num = 0

					compile_arithmetic()
					break
				
				continue

	compile_arithmetic()

	def interperet(itokens):
		
		used_token = False
		skip_index = 0
		pre_index = 0
		func = False
		loop = False
		
		for xindex, token in enumerate(itokens):
			index = xindex
			
			if used_token == True:
				used_token = False
				continue
				
			if not index >= skip_index:
				continue
			
			if "print" in token and func == False:
				if itokens[index+1] == "sys.newline":
					print("\n")
					continue
		
				if itokens[index+1] == "sys.input":
					print(input(itokens[index+2]))
					used_token = True
					continue
				
				if itokens[index+1] == "var":
					print(variables[itokens[index+2]], end = '')
					skip_index = index + 2
					continue
				
				else:
					print(itokens[index+1])
					used_token = True
					continue
		
			if "func" in token:
				if func == False:
					func = True
			
				else:
					print("Cannot assign a function in a function")
			
				func_name = itokens[index+1]
				skip_index = index
		
				for findex, ftoken in enumerate(itokens[skip_index:]):
					if ftoken != func_name and ftoken != "func":
						func_tokens[func_name].append(ftoken)
						skip_index += 1
		
						if ftoken == "}":
							break
					
					else:
						continue
				
				skip_index = skip_index - 8
				pre_index = index
				func = False
		
				continue
			
			if "call" in token:
				func_name = itokens[index+1]
				args = itokens[index+2]
		
				if len(args.split(",")) == len(func_tokens[func_name][0]["args"]):
					pass
		
				else:
					if func_tokens[func_name][0]["args"] != "()":
						pass
		
					else:
						print("invalid function arguments: ", func_name)
						continue
		
				cargs = args.replace("(","").replace(")","").replace(" ","").split(",")
		
				#try:
				if True:
					for cfindex, cftoken in enumerate(cargs):
						if cftoken != "":
							variables[func_tokens[func_name][0]["args"][cfindex]] = cftoken
		
					if len(func_tokens[func_name]) > 0:
					
						for cindex, tok in enumerate(func_tokens[func_name]):
							#print(tok)
							if used_token == True:
								used_token = False
								
								continue
							
							if "print" in tok:
								if func_tokens[func_name][cindex+1] == "sys.newline":
									print("\n")
									continue
								
								if func_tokens[func_name][cindex+1] == "sys.input":
									print(input(func_tokens[func_name][cindex+2]))
									used_token = True
									continue
								
								if func_tokens[func_name][cindex+1] == "var":
									print(variables[func_tokens[func_name][cindex+2]], end = '')
								
								else:
									print(func_tokens[func_name][cindex+1], end = '')
									used_token = True
		
									
				#except Exception as e:
				#	print("invalid function arguments: {} | {}".format(func_name, e))
			
			if token == "loop":
				loop_name = itokens[index+1]
				lskip_index = index
		
				for findex, ftoken in enumerate(tokens[lskip_index:]):
					if ftoken != loop_name:
						loop_tokens[loop_name].append(ftoken)
						lskip_index += 1
		
						if ftoken == "}":
							break
					
					else:
						continue
				
				lskip_index = lskip_index - 8
				pre_index = index
				loop = False
		
				continue
			
			if token == "run":
				loop_name = itokens[index+1]
				args = itokens[index+2]
		
				if len(args.split(",")) == len(loop_tokens[loop_name][0]["args"]):
					pass
		
				else:
					if loop_tokens[loop_name][0]["args"] != "()":
						pass
		
					else:
						print("invalid function arguments: ", loop_name)
						continue
		
				cargs = args.replace("(","").replace(")","").replace(" ","").split(",")
		
				#try:
				if True:
					for lindex in range(int(cargs[0])):
			
						if len(loop_tokens[loop_name]) > 0:
						
							for cindex, tok in enumerate(loop_tokens[loop_name]):
								
								if used_token == True:
									used_token = False
									
									continue
								
								if "print" in tok:
									if loop_tokens[loop_name][cindex+1] == "sys.newline":
										print("\n")
										continue
		
									if loop_tokens[loop_name][cindex+1] == "sys.input":
										print(input(loop_tokens[loop_name][cindex+2]))
										used_token = True
										continue
									
									if loop_tokens[loop_name][cindex+1] == "var":
										print(variables[loop_tokens[loop_name][cindex+2]], end = '')
									
									else:
										print(loop_tokens[loop_name][cindex+1], end = '')
										used_token = True
									
				#except Exception as e:
				#	print("invalid loop arguments: {} | {}".format(loop_name, e))

	def base_execute(jade):
		contents = jade
		arguments = ""
		
		num = 0
		skip_index = 0
		lskip_index = 0
		
		func = False
		args = False
		loop = False
		comment = False
		used_num = False
		used_token = False
		used_variable = False
		
		func_tokens = {}
		loop_tokens = {}
		variables = {}
		if_cache = []
		compiled = {}


		tokens = []
		
		token = ""
		string = ""
		integer = ""

		is_int = False
		is_str = False

	# --// Parse file contents
		
		for char in contents:

	# --// Get strings

			if char == "#":
				comment = True
			
			if char in str_tokens:
				if is_str == False:
					is_str = True

				elif is_str == True:
					is_str = False
					tokens.append(string)
					string = ""
					
					continue
			
				continue

			if char == "(" and is_str == False:
				if tokens != "":
					tokens.append(token)
					token = ""
				
				args = True
				arguments += char
				continue

			if char == ")" and is_str == False:
				args = False
				arguments += char

				tokens.append(arguments)
				arguments = ""
				
				continue

	# --// Check for a string

			if args == True:
				arguments += char
				continue
			
			if is_str == True:
				string += char
				continue

	# --// Check for arethmatic
			if char in int_tokens:
				if is_int == False:
					is_int = True

					integer += char

					continue

				integer += char
				token = ""

				continue

			if is_int == True:
				is_int = False
				tokens.append(integer)
				integer = ""
			
			if char in math_tokens:
				tokens.append(char)

				token = ""

				continue

	# --// Check for end line

			if comment == True:
				if char != "\n":
					continue

				else:
					comment = False
					continue
				
			if char in end_tokens:
				tokens.append(token)
				token = ""
				continue

		for index, token in enumerate(tokens):
			if used_variable == True:
				used_variable = False
				continue
			
			if token == "=":
				if used_variable == True:
					print("Cannot assign an assigned value")
					
				else:
					if tokens[index+1] == "sys.input":
						variables[tokens[index-1]] = input(tokens[index+2])
						used_variable = True
						continue
		
					if tokens[index+1] == "sys.read":
						with open(tokens[index+2], "r") as sysread:
							variables[tokens[index-1]] = sysread.read()
							
						used_variable = True
						continue
		
					else:
						variables[tokens[index-1]] = tokens[index+1]
						used_variable = True
		
		# --// Compile Files
		
		for index, token in enumerate(tokens):
			if used_variable == True:
				used_variable = False
				continue
			
			if token == "sys.write":
				with open(tokens[index+1], "w") as syswrite:
					syswrite.write(tokens[index+2])
		
				used_variable = True
				
		# --// show parsed tokens
		
		#print("Variable parse: ", tokens)
		#print("Variable tree: ", variables)
		
		# --// Compile arguments
		
		for index, token in enumerate(tokens):
			if "(" in token and ")" in token and tokens[index-1] == "if":
				if_cache = []
		
				args = token.replace("(","").replace(")","").split(" ")
		
				if args[0] == "var":
					if variables[args[1]].replace('.','',1).isdigit():
						arg1 = float(variables[args[1]])
						
					else:
						arg1 = variables[args[1]]
		
					if args[3] == "var":
						if variables[args[4]].replace('.','',1).isdigit():
							arg2 = float(variables[args[4]])
							
						else:
							arg2 = variables[args[4]]
						
					else:
						if args[3].replace('.','',1).isdigit():
							arg2 = float(args[3])
							
						else:
							arg2 = args[3]
		
				else:
					if args[0].replace('.','',1).isdigit():
						arg1 = float(args[0])
						
					else:
						arg1 = args[0]
		
					if args[2] == "var":
						if variables[args[3]].replace('.','',1).isdigit():
							arg2 = float(variables[args[3]])
							
						else:
							arg2 = variables[args[3]]
			
					else:
						if args[2].replace('.','',1).isdigit():
							arg2 = float(args[2])
							
						else:
							arg2 = args[2]
		
				if args[0] == "var":
					expr = args[2]
		
				else:
					expr = args[1]
				
				for arg in tokens[index:]:
					if arg != "}":
						if_cache.append(arg)
					
					else:
						break
		
				if expr == "==":
					if arg1 == arg2:
						interperet(if_cache[2:])
		
				if expr == ">=":
					if arg1 >= arg2:
						interperet(if_cache[2:])
					
				if expr == "<=":
					if arg1 <= arg2:
						interperet(if_cache[2:])
					
				if expr == "!=":
					if arg1 != arg2:
						interperet(if_cache[2:])
		
		for index, token in enumerate(tokens):
			if "(" in token and ")" in token and tokens[index-2] == "func":
				func_name = tokens[index-1]
				
				func_tokens[func_name] = []
				func_tokens[func_name].append({})
				func_tokens[func_name][0]["args"] = []
				
				for arg in token[1:-1].split(","):
					if arg != "":
						func_tokens[func_name][0]["args"].append(arg)
		
		for index, token in enumerate(tokens):
			if "(" in token and ")" in token and tokens[index-2] == "loop":
				loop_name = tokens[index-1]
				
				loop_tokens[loop_name] = []
				loop_tokens[loop_name].append({})
				loop_tokens[loop_name][0]["args"] = []
				
				for arg in token[1:-1].split(","):
					if arg != "":
						loop_tokens[loop_name][0]["args"].append(arg)
						
		# --// Lexer
		
		for index, token in enumerate(tokens):
			if used_token == True:
				used_token = False
				continue
				
			if not index >= skip_index:
				continue
			
			if token == "print" and func == False:
				if tokens[index+1] == "sys.newline":
					print("\n")
					continue
		
				if tokens[index+1] == "sys.input":
					print(input(tokens[index+2]))
					used_token = True
					continue
				
				if tokens[index+1] == "var":
					print(variables[tokens[index+2]], end = '')
					skip_index = index + 2
					continue
				
				else:
					print(tokens[index+1])
					used_token = True
					continue
		
			if token == "func":
				if func == False:
					func = True
			
				else:
					print("Cannot assign a function in a function")
			
				func_name = tokens[index+1]
				skip_index = index
		
				for findex, ftoken in enumerate(tokens[skip_index:]):
					if ftoken != func_name and ftoken != "func":
						func_tokens[func_name].append(ftoken)
						skip_index += 1
		
						if ftoken == "}":
							break
					
					else:
						continue
				
				skip_index = skip_index - 8
				pre_index = index
				func = False
		
				continue
			
			if token == "call":
				func_name = tokens[index+1]
				args = tokens[index+2]
		
				if len(args.split(",")) == len(func_tokens[func_name][0]["args"]):
					pass
		
				else:
					if func_tokens[func_name][0]["args"] != "()":
						pass
		
					else:
						print("invalid function arguments: ", func_name)
						continue
		
				cargs = args.replace("(","").replace(")","").replace(" ","").split(",")
		
				#try:
				if True:
					for cfindex, cftoken in enumerate(cargs):
						if cftoken != "":
							variables[func_tokens[func_name][0]["args"][cfindex]] = cftoken
		
					if len(func_tokens[func_name]) > 0:
					
						for cindex, tok in enumerate(func_tokens[func_name]):
							#print(tok)
							if used_token == True:
								used_token = False
								
								continue
							
							if "print" in tok:
								if func_tokens[func_name][cindex+1] == "sys.newline":
									print("\n")
									continue
								
								if func_tokens[func_name][cindex+1] == "sys.input":
									print(input(func_tokens[func_name][cindex+2]))
									used_token = True
									continue
								
								if func_tokens[func_name][cindex+1] == "var":
									print(variables[func_tokens[func_name][cindex+2]], end = '')
								
								else:
									print(func_tokens[func_name][cindex+1], end = '')
									used_token = True
		
									
				#except Exception as e:
				#	print("invalid function arguments: {} | {}".format(func_name, e))
			
			if token == "loop":
				loop_name = tokens[index+1]
				lskip_index = index
		
				for findex, ftoken in enumerate(tokens[lskip_index:]):
					if ftoken != loop_name:
						loop_tokens[loop_name].append(ftoken)
						lskip_index += 1
		
						if ftoken == "}":
							break
					
					else:
						continue
				
				lskip_index = lskip_index - 8
				pre_index = index
				loop = False
		
				continue
			
			if token == "run":
				loop_name = tokens[index+1]
				args = tokens[index+2]
		
				if len(args.split(",")) == len(loop_tokens[loop_name][0]["args"]):
					pass
		
				else:
					if loop_tokens[loop_name][0]["args"] != "()":
						pass
		
					else:
						print("invalid function arguments: ", loop_name)
						continue
		
				cargs = args.replace("(","").replace(")","").replace(" ","").split(",")
		
				#try:
				if True:
					for lindex in range(int(cargs[0])):
			
						if len(loop_tokens[loop_name]) > 0:
						
							for cindex, tok in enumerate(loop_tokens[loop_name]):
								
								if used_token == True:
									used_token = False
									
									continue
								
								if "print" in tok:
									if loop_tokens[loop_name][cindex+1] == "sys.newline":
										print("\n")
										continue
		
									if loop_tokens[loop_name][cindex+1] == "sys.input":
										print(input(loop_tokens[loop_name][cindex+2]))
										used_token = True
										continue
									
									if loop_tokens[loop_name][cindex+1] == "var":
										print(variables[loop_tokens[loop_name][cindex+2]], end = '')
									
									else:
										print(loop_tokens[loop_name][cindex+1], end = '')
										used_token = True
									
				#except Exception as e:
				#	print("invalid loop arguments: {} | {}".format(loop_name, e))
		
		#print(variables)
		#print(func_tokens)
		#print("\n\n\n")
		#print(tokens)
										
	# --// Show parsed tokens

	#print("Arithmetic parse: ", tokens)

	# --// Compile variables

	for index, token in enumerate(tokens):
		if used_variable == True:
			used_variable = False
			continue
		
		if token == "=":
			if used_variable == True:
				print("Cannot assign an assigned value")
				
			else:
				if tokens[index+1] == "sys.input":
					variables[tokens[index-1]] = input(tokens[index+2])
					used_variable = True
					continue

				if tokens[index+1] == "sys.read":
					with open(tokens[index+2], "r") as sysread:
						variables[tokens[index-1]] = sysread.read()
						
					used_variable = True
					continue

				else:
					variables[tokens[index-1]] = tokens[index+1]
					used_variable = True

	# --// Compile Files

	for index, token in enumerate(tokens):
		if used_variable == True:
			used_variable = False
			continue
		
		if token == "sys.write":
			with open(tokens[index+1], "w") as syswrite:
				syswrite.write(tokens[index+2])

			used_variable = True
			
	# --// show parsed tokens

	#print("Variable parse: ", tokens)
	#print("Variable tree: ", variables)

	# --// Compile arguments

	for index, token in enumerate(tokens):
		if "(" in token and ")" in token and tokens[index-1] == "if":
			if_cache = []

			args = token.replace("(","").replace(")","").split(" ")

			if args[0] == "var":
				if variables[args[1]].replace('.','',1).isdigit():
					arg1 = float(variables[args[1]])
					
				else:
					arg1 = variables[args[1]]

				if args[3] == "var":
					if variables[args[4]].replace('.','',1).isdigit():
						arg2 = float(variables[args[4]])
						
					else:
						arg2 = variables[args[4]]
					
				else:
					if args[3].replace('.','',1).isdigit():
						arg2 = float(args[3])
						
					else:
						arg2 = args[3]

			else:
				if args[0].replace('.','',1).isdigit():
					arg1 = float(args[0])
					
				else:
					arg1 = args[0]

				if args[2] == "var":
					if variables[args[3]].replace('.','',1).isdigit():
						arg2 = float(variables[args[3]])
						
					else:
						arg2 = variables[args[3]]
		
				else:
					if args[2].replace('.','',1).isdigit():
						arg2 = float(args[2])
						
					else:
						arg2 = args[2]

			if args[0] == "var":
				expr = args[2]

			else:
				expr = args[1]
			
			for arg in tokens[index:]:
				if arg != "}":
					if_cache.append(arg)
				
				else:
					break

			if expr == "==":
				if arg1 == arg2:
					interperet(if_cache[2:])

			if expr == ">=":
				if arg1 >= arg2:
					interperet(if_cache[2:])
				
			if expr == "<=":
				if arg1 <= arg2:
					interperet(if_cache[2:])
				
			if expr == "!=":
				if arg1 != arg2:
					interperet(if_cache[2:])

	for index, token in enumerate(tokens):
		if "(" in token and ")" in token and tokens[index-2] == "func":
			func_name = tokens[index-1]
			
			func_tokens[func_name] = []
			func_tokens[func_name].append({})
			func_tokens[func_name][0]["args"] = []
			
			for arg in token[1:-1].split(","):
				if arg != "":
					func_tokens[func_name][0]["args"].append(arg)

	for index, token in enumerate(tokens):
		if "(" in token and ")" in token and tokens[index-2] == "loop":
			loop_name = tokens[index-1]
			
			loop_tokens[loop_name] = []
			loop_tokens[loop_name].append({})
			loop_tokens[loop_name][0]["args"] = []
			
			for arg in token[1:-1].split(","):
				if arg != "":
					loop_tokens[loop_name][0]["args"].append(arg)
					
	# --// Lexer

	for index, token in enumerate(tokens):
		if used_token == True:
			used_token = False
			continue
			
		if not index >= skip_index:
			continue
		
		if token == "print" and func == False:
			if tokens[index+1] == "sys.newline":
				print("\n")
				continue

			if tokens[index+1] == "sys.input":
				print(input(tokens[index+2]))
				used_token = True
				continue
			
			if tokens[index+1] == "var":
				print(variables[tokens[index+2]], end = '')
				skip_index = index + 2
				continue
			
			else:
				print(tokens[index+1])
				used_token = True
				continue

		if token == "func":
			if func == False:
				func = True
		
			else:
				print("Cannot assign a function in a function")
		
			func_name = tokens[index+1]
			skip_index = index

			for findex, ftoken in enumerate(tokens[skip_index:]):
				if ftoken != func_name and ftoken != "func":
					func_tokens[func_name].append(ftoken)
					skip_index += 1

					if ftoken == "}":
						break
				
				else:
					continue
			
			skip_index = skip_index - 8
			pre_index = index
			func = False

			continue
		
		if token == "call":
			func_name = tokens[index+1]
			args = tokens[index+2]

			if len(args.split(",")) == len(func_tokens[func_name][0]["args"]):
				pass

			else:
				if func_tokens[func_name][0]["args"] != "()":
					pass

				else:
					print("invalid function arguments: ", func_name)
					continue

			cargs = args.replace("(","").replace(")","").replace(" ","").split(",")

			#try:
			if True:
				for cfindex, cftoken in enumerate(cargs):
					if cftoken != "":
						variables[func_tokens[func_name][0]["args"][cfindex]] = cftoken

				if len(func_tokens[func_name]) > 0:
				
					for cindex, tok in enumerate(func_tokens[func_name]):
						#print(tok)
						if used_token == True:
							used_token = False
							
							continue
						
						if "print" in tok:
							if func_tokens[func_name][cindex+1] == "sys.newline":
								print("\n")
								continue
							
							if func_tokens[func_name][cindex+1] == "sys.input":
								print(input(func_tokens[func_name][cindex+2]))
								used_token = True
								continue
							
							if func_tokens[func_name][cindex+1] == "var":
								print(variables[func_tokens[func_name][cindex+2]], end = '')
							
							else:
								print(func_tokens[func_name][cindex+1], end = '')
								used_token = True

								
			#except Exception as e:
			#	print("invalid function arguments: {} | {}".format(func_name, e))
		
		if token == "loop":
			loop_name = tokens[index+1]
			lskip_index = index

			for findex, ftoken in enumerate(tokens[lskip_index:]):
				if ftoken != loop_name:
					loop_tokens[loop_name].append(ftoken)
					lskip_index += 1

					if ftoken == "}":
						break
				
				else:
					continue
			
			lskip_index = lskip_index - 8
			pre_index = index
			loop = False

			continue

		if token == "exec":
			used_token = True

			base_execute(tokens[index+1])
			continue
		
		if token == "run":
			loop_name = tokens[index+1]
			args = tokens[index+2]

			if len(args.split(",")) == len(loop_tokens[loop_name][0]["args"]):
				pass

			else:
				if loop_tokens[loop_name][0]["args"] != "()":
					pass

				else:
					print("invalid function arguments: ", loop_name)
					continue

			cargs = args.replace("(","").replace(")","").replace(" ","").split(",")

			#try:
			if True:
				for lindex in range(int(cargs[0])):
		
					if len(loop_tokens[loop_name]) > 0:
					
						for cindex, tok in enumerate(loop_tokens[loop_name]):
							
							if used_token == True:
								used_token = False
								
								continue
							
							if "print" in tok:
								if loop_tokens[loop_name][cindex+1] == "sys.newline":
									print("\n")
									continue

								if loop_tokens[loop_name][cindex+1] == "sys.input":
									print(input(loop_tokens[loop_name][cindex+2]))
									used_token = True
									continue
								
								if loop_tokens[loop_name][cindex+1] == "var":
									print(variables[loop_tokens[loop_name][cindex+2]], end = '')
								
								else:
									print(loop_tokens[loop_name][cindex+1], end = '')
									used_token = True
								
			#except Exception as e:
			#	print("invalid loop arguments: {} | {}".format(loop_name, e))

	#print(variables)
	#print(func_tokens)
	#print("\n\n\n")
	#print(tokens)

else:
	with open(file, "r") as jde:
		contents = jde.read()

		tokens = []
		
		token = ""
		string = ""
		integer = ""

		is_int = False
		is_str = False

	# --// Parse file contents
		
		for char in contents:

	# --// Get strings

			if char == "#":
				print("[ Jade ] Comment, skipping line")
				comment = True
			
			if char in str_tokens:
				print("[ Jade ] String token found")
				if is_str == False:
					is_str = True

				elif is_str == True:
					is_str = False
					tokens.append(string)
					string = ""
					
					continue
			
				continue

			if char == "(" and is_str == False:
				print("[ Jade ] Argument token found")
				if tokens != "":
					tokens.append(token)
					token = ""
				
				args = True
				arguments += char
				continue

			if char == ")" and is_str == False:
				print("[ Jade ] Argument token found")
				args = False
				arguments += char

				tokens.append(arguments)
				arguments = ""
				
				continue

	# --// Check for a string

			if args == True:
				arguments += char
				continue
			
			if is_str == True:
				string += char
				continue

	# --// Check for arethmatic
			if char in int_tokens:
				print("[ Jade ] Integer token found")
				if is_int == False:
					is_int = True

					integer += char

					continue

				integer += char
				token = ""

				continue

			if is_int == True:
				is_int = False
				tokens.append(integer)
				integer = ""
			
			if char in math_tokens:
				print("[ Jade ] Math token found")
				tokens.append(char)

				token = ""

				continue

	# --// Check for end line

			if comment == True:
				if char != "\n":
					print("[ Jade ] Clearing comment")
					continue

				else:
					comment = False
					continue
				
			if char in end_tokens:
				print("[ Jade ] End token")
				tokens.append(token)
				token = ""
				continue

	# --// Append to token
			
			token += char

	# --// Remove empty tokens

	print("[ Jade ] Filtering glitched / empty tokens")

	for index, token in enumerate(tokens):
		if token == "" or token == "\n" or token == "":
			tokens.pop(index)

	# --// Show parsed tokens

	print("[ Jade ] Raw Parse: ", tokens)

	# --// Compile raw data

	def compile_arithmetic():
		print("[ Jade ] Compiling arithmetic")

		global used_num
		global num
		global tokens

	# --// Parse
		
		for index, token in enumerate(tokens):
			
			if used_num == True:
				used_num = False
				continue

	# --// Check for arithmetic tokens
			
			if token in math_tokens:
				if token == "+":
					num = str(float(tokens[index-1])+float(tokens[index+1]))
					tokens[index] = num
					tokens.pop(index-1)
					tokens.pop(index)
					
					num = 0
					
					compile_arithmetic()
					break

	# --// Subtraction
				
				if token == "-":
					num = str(float(tokens[index-1])-float(tokens[index+1]))
					tokens[index] = num
					tokens.pop(index-1)
					tokens.pop(index)
					
					num = 0
					
					compile_arithmetic()
					break

	# --// Multiplication
				
				if token == "*":
					num = str(float(tokens[index-1])*float(tokens[index+1]))
					tokens[index] = num
					tokens.pop(index-1)
					tokens.pop(index)
					
					num = 0
					
					compile_arithmetic()
					break

	# --// Division
				
				if token == "/":
					num = str(float(tokens[index-1])/float(tokens[index+1]))
					tokens[index] = num
					tokens.pop(index-1)
					tokens.pop(index)
		
					num = 0

					compile_arithmetic()
					break

	# --// Exponenets
					
				if token == "^":
					num = str(float(tokens[index-1])^float(tokens[index+1]))
					tokens[index] = num
					tokens.pop(index-1)
					tokens.pop(index)
		
					num = 0

					compile_arithmetic()
					break
				
				continue

	compile_arithmetic()

	def interperet(itokens):
		print("[ Jade ] Interpreting")
		
		used_token = False
		skip_index = 0
		pre_index = 0
		func = False
		loop = False
		
		for xindex, token in enumerate(itokens):
			index = xindex
			
			if used_token == True:
				used_token = False
				continue
				
			if not index >= skip_index:
				continue
			
			if "print" in token and func == False:
				print("[ Jade ] I/O operation")
				if itokens[index+1] == "sys.newline":
					print("\n")
					continue
		
				if itokens[index+1] == "sys.input":
					print(input(itokens[index+2]))
					used_token = True
					continue
				
				if itokens[index+1] == "var":
					print(variables[itokens[index+2]], end = '')
					skip_index = index + 2
					continue
				
				else:
					print(itokens[index+1])
					used_token = True
					continue
		
			if "func" in token:
				print("[ Jade ] Function")
				if func == False:
					func = True
			
				else:
					print("Cannot assign a function in a function")
			
				func_name = itokens[index+1]
				skip_index = index
		
				for findex, ftoken in enumerate(itokens[skip_index:]):
					if ftoken != func_name and ftoken != "func":
						func_tokens[func_name].append(ftoken)
						skip_index += 1
		
						if ftoken == "}":
							break
					
					else:
						continue
				
				skip_index = skip_index - 8
				pre_index = index
				func = False
		
				continue
			
			if "call" in token:
				print("[ Jade ] Function call")

				func_name = itokens[index+1]
				args = itokens[index+2]
		
				if len(args.split(",")) == len(func_tokens[func_name][0]["args"]):
					pass
		
				else:
					if func_tokens[func_name][0]["args"] != "()":
						pass
		
					else:
						print("invalid function arguments: ", func_name)
						continue
		
				cargs = args.replace("(","").replace(")","").replace(" ","").split(",")
		
				#try:
				if True:
					for cfindex, cftoken in enumerate(cargs):
						if cftoken != "":
							variables[func_tokens[func_name][0]["args"][cfindex]] = cftoken
		
					if len(func_tokens[func_name]) > 0:
					
						for cindex, tok in enumerate(func_tokens[func_name]):
							#print(tok)
							if used_token == True:
								used_token = False
								
								continue
							
							if "print" in tok:
								if func_tokens[func_name][cindex+1] == "sys.newline":
									print("\n")
									continue
								
								if func_tokens[func_name][cindex+1] == "sys.input":
									print(input(func_tokens[func_name][cindex+2]))
									used_token = True
									continue
								
								if func_tokens[func_name][cindex+1] == "var":
									print(variables[func_tokens[func_name][cindex+2]], end = '')
								
								else:
									print(func_tokens[func_name][cindex+1], end = '')
									used_token = True
		
									
				#except Exception as e:
				#	print("invalid function arguments: {} | {}".format(func_name, e))
			
			if token == "loop":
				print("[ Jade ] Loop")

				loop_name = itokens[index+1]
				lskip_index = index
		
				for findex, ftoken in enumerate(tokens[lskip_index:]):
					if ftoken != loop_name:
						loop_tokens[loop_name].append(ftoken)
						lskip_index += 1
		
						if ftoken == "}":
							break
					
					else:
						continue
				
				lskip_index = lskip_index - 8
				pre_index = index
				loop = False
		
				continue
			
			if token == "run":
				print("[ Jade ] Loop call")

				loop_name = itokens[index+1]
				args = itokens[index+2]
		
				if len(args.split(",")) == len(loop_tokens[loop_name][0]["args"]):
					pass
		
				else:
					if loop_tokens[loop_name][0]["args"] != "()":
						pass
		
					else:
						print("invalid function arguments: ", loop_name)
						continue
		
				cargs = args.replace("(","").replace(")","").replace(" ","").split(",")
		
				#try:
				if True:
					for lindex in range(int(cargs[0])):
			
						if len(loop_tokens[loop_name]) > 0:
						
							for cindex, tok in enumerate(loop_tokens[loop_name]):
								
								if used_token == True:
									used_token = False
									
									continue
								
								if "print" in tok:
									if loop_tokens[loop_name][cindex+1] == "sys.newline":
										print("\n")
										continue
		
									if loop_tokens[loop_name][cindex+1] == "sys.input":
										print(input(loop_tokens[loop_name][cindex+2]))
										used_token = True
										continue
									
									if loop_tokens[loop_name][cindex+1] == "var":
										print(variables[loop_tokens[loop_name][cindex+2]], end = '')
									
									else:
										print(loop_tokens[loop_name][cindex+1], end = '')
										used_token = True
									
				#except Exception as e:
				#	print("invalid loop arguments: {} | {}".format(loop_name, e))

	def base_execute(jade):
		print("[ Jade ] Re-Executing base")

		contents = jade
		arguments = ""
		
		num = 0
		skip_index = 0
		lskip_index = 0
		
		func = False
		args = False
		loop = False
		comment = False
		used_num = False
		used_token = False
		used_variable = False
		
		func_tokens = {}
		loop_tokens = {}
		variables = {}
		if_cache = []
		compiled = {}


		tokens = []
		
		token = ""
		string = ""
		integer = ""

		is_int = False
		is_str = False

	# --// Parse file contents
		
		for char in contents:

	# --// Get strings

			if char == "#":
				comment = True
			
			if char in str_tokens:
				if is_str == False:
					is_str = True

				elif is_str == True:
					is_str = False
					tokens.append(string)
					string = ""
					
					continue
			
				continue

			if char == "(" and is_str == False:
				if tokens != "":
					tokens.append(token)
					token = ""
				
				args = True
				arguments += char
				continue

			if char == ")" and is_str == False:
				args = False
				arguments += char

				tokens.append(arguments)
				arguments = ""
				
				continue

	# --// Check for a string

			if args == True:
				arguments += char
				continue
			
			if is_str == True:
				string += char
				continue

	# --// Check for arethmatic
			if char in int_tokens:
				if is_int == False:
					is_int = True

					integer += char

					continue

				integer += char
				token = ""

				continue

			if is_int == True:
				is_int = False
				tokens.append(integer)
				integer = ""
			
			if char in math_tokens:
				tokens.append(char)

				token = ""

				continue

	# --// Check for end line

			if comment == True:
				if char != "\n":
					continue

				else:
					comment = False
					continue
				
			if char in end_tokens:
				tokens.append(token)
				token = ""
				continue

		for index, token in enumerate(tokens):
			if used_variable == True:
				used_variable = False
				continue
			
			if token == "=":
				if used_variable == True:
					print("[ Jade ] Cannot assign an assigned value")
					
				else:
					if tokens[index+1] == "sys.input":
						variables[tokens[index-1]] = input(tokens[index+2])
						used_variable = True
						continue
		
					if tokens[index+1] == "sys.read":
						with open(tokens[index+2], "r") as sysread:
							variables[tokens[index-1]] = sysread.read()
							
						used_variable = True
						continue
		
					else:
						variables[tokens[index-1]] = tokens[index+1]
						used_variable = True
		
		# --// Compile Files
		
		for index, token in enumerate(tokens):
			if used_variable == True:
				used_variable = False
				continue
			
			if token == "sys.write":
				with open(tokens[index+1], "w") as syswrite:
					syswrite.write(tokens[index+2])
		
				used_variable = True
				
		# --// show parsed tokens
		
		print("[ Jade ] Variable parse: ", tokens)
		print("[ Jade ] Variable tree: ", variables)
		
		# --// Compile arguments
		
		for index, token in enumerate(tokens):
			if "(" in token and ")" in token and tokens[index-1] == "if":
				if_cache = []
		
				args = token.replace("(","").replace(")","").split(" ")
		
				if args[0] == "var":
					if variables[args[1]].replace('.','',1).isdigit():
						arg1 = float(variables[args[1]])
						
					else:
						arg1 = variables[args[1]]
		
					if args[3] == "var":
						if variables[args[4]].replace('.','',1).isdigit():
							arg2 = float(variables[args[4]])
							
						else:
							arg2 = variables[args[4]]
						
					else:
						if args[3].replace('.','',1).isdigit():
							arg2 = float(args[3])
							
						else:
							arg2 = args[3]
		
				else:
					if args[0].replace('.','',1).isdigit():
						arg1 = float(args[0])
						
					else:
						arg1 = args[0]
		
					if args[2] == "var":
						if variables[args[3]].replace('.','',1).isdigit():
							arg2 = float(variables[args[3]])
							
						else:
							arg2 = variables[args[3]]
			
					else:
						if args[2].replace('.','',1).isdigit():
							arg2 = float(args[2])
							
						else:
							arg2 = args[2]
		
				if args[0] == "var":
					expr = args[2]
		
				else:
					expr = args[1]
				
				for arg in tokens[index:]:
					if arg != "}":
						if_cache.append(arg)
					
					else:
						break
		
				if expr == "==":
					if arg1 == arg2:
						interperet(if_cache[2:])
		
				if expr == ">=":
					if arg1 >= arg2:
						interperet(if_cache[2:])
					
				if expr == "<=":
					if arg1 <= arg2:
						interperet(if_cache[2:])
					
				if expr == "!=":
					if arg1 != arg2:
						interperet(if_cache[2:])
		
		for index, token in enumerate(tokens):
			if "(" in token and ")" in token and tokens[index-2] == "func":
				func_name = tokens[index-1]
				
				func_tokens[func_name] = []
				func_tokens[func_name].append({})
				func_tokens[func_name][0]["args"] = []
				
				for arg in token[1:-1].split(","):
					if arg != "":
						func_tokens[func_name][0]["args"].append(arg)
		
		for index, token in enumerate(tokens):
			if "(" in token and ")" in token and tokens[index-2] == "loop":
				loop_name = tokens[index-1]
				
				loop_tokens[loop_name] = []
				loop_tokens[loop_name].append({})
				loop_tokens[loop_name][0]["args"] = []
				
				for arg in token[1:-1].split(","):
					if arg != "":
						loop_tokens[loop_name][0]["args"].append(arg)
						
		# --// Lexer
		
		for index, token in enumerate(tokens):
			if used_token == True:
				used_token = False
				continue
				
			if not index >= skip_index:
				continue
			
			if token == "print" and func == False:
				if tokens[index+1] == "sys.newline":
					print("\n")
					continue
		
				if tokens[index+1] == "sys.input":
					print(input(tokens[index+2]))
					used_token = True
					continue
				
				if tokens[index+1] == "var":
					print(variables[tokens[index+2]], end = '')
					skip_index = index + 2
					continue
				
				else:
					print(tokens[index+1])
					used_token = True
					continue
		
			if token == "func":
				if func == False:
					func = True
			
				else:
					print("[ Jade ] Cannot assign a function in a function")
			
				func_name = tokens[index+1]
				skip_index = index
		
				for findex, ftoken in enumerate(tokens[skip_index:]):
					if ftoken != func_name and ftoken != "func":
						func_tokens[func_name].append(ftoken)
						skip_index += 1
		
						if ftoken == "}":
							break
					
					else:
						continue
				
				skip_index = skip_index - 8
				pre_index = index
				func = False
		
				continue
			
			if token == "call":
				func_name = tokens[index+1]
				args = tokens[index+2]
		
				if len(args.split(",")) == len(func_tokens[func_name][0]["args"]):
					pass
		
				else:
					if func_tokens[func_name][0]["args"] != "()":
						pass
		
					else:
						print("[ Jade ] invalid function arguments: ", func_name)
						continue
		
				cargs = args.replace("(","").replace(")","").replace(" ","").split(",")
		
				#try:
				if True:
					for cfindex, cftoken in enumerate(cargs):
						if cftoken != "":
							variables[func_tokens[func_name][0]["args"][cfindex]] = cftoken
		
					if len(func_tokens[func_name]) > 0:
					
						for cindex, tok in enumerate(func_tokens[func_name]):
							#print(tok)
							if used_token == True:
								used_token = False
								
								continue
							
							if "print" in tok:
								if func_tokens[func_name][cindex+1] == "sys.newline":
									print("\n")
									continue
								
								if func_tokens[func_name][cindex+1] == "sys.input":
									print(input(func_tokens[func_name][cindex+2]))
									used_token = True
									continue
								
								if func_tokens[func_name][cindex+1] == "var":
									print(variables[func_tokens[func_name][cindex+2]], end = '')
								
								else:
									print(func_tokens[func_name][cindex+1], end = '')
									used_token = True
		
									
				#except Exception as e:
				#	print("invalid function arguments: {} | {}".format(func_name, e))
			
			if token == "loop":
				loop_name = tokens[index+1]
				lskip_index = index
		
				for findex, ftoken in enumerate(tokens[lskip_index:]):
					if ftoken != loop_name:
						loop_tokens[loop_name].append(ftoken)
						lskip_index += 1
		
						if ftoken == "}":
							break
					
					else:
						continue
				
				lskip_index = lskip_index - 8
				pre_index = index
				loop = False
		
				continue
			
			if token == "run":
				loop_name = tokens[index+1]
				args = tokens[index+2]
		
				if len(args.split(",")) == len(loop_tokens[loop_name][0]["args"]):
					pass
		
				else:
					if loop_tokens[loop_name][0]["args"] != "()":
						pass
		
					else:
						print("[ Jade ] invalid function arguments: ", loop_name)
						continue
		
				cargs = args.replace("(","").replace(")","").replace(" ","").split(",")
		
				#try:
				if True:
					for lindex in range(int(cargs[0])):
			
						if len(loop_tokens[loop_name]) > 0:
						
							for cindex, tok in enumerate(loop_tokens[loop_name]):
								
								if used_token == True:
									used_token = False
									
									continue
								
								if "print" in tok:
									if loop_tokens[loop_name][cindex+1] == "sys.newline":
										print("\n")
										continue
		
									if loop_tokens[loop_name][cindex+1] == "sys.input":
										print(input(loop_tokens[loop_name][cindex+2]))
										used_token = True
										continue
									
									if loop_tokens[loop_name][cindex+1] == "var":
										print(variables[loop_tokens[loop_name][cindex+2]], end = '')
									
									else:
										print(loop_tokens[loop_name][cindex+1], end = '')
										used_token = True
									
				#except Exception as e:
				#	print("invalid loop arguments: {} | {}".format(loop_name, e))
		
		print(variables)
		print(func_tokens)
		print("\n\n\n")
		print(tokens)
										
	# --// Show parsed tokens

	print("[ Jade ] Arithmetic parse: ", tokens)

	# --// Compile variables

	for index, token in enumerate(tokens):
		if used_variable == True:
			used_variable = False
			continue
		
		if token == "=":
			if used_variable == True:
				print("[ Jade ] Cannot assign an assigned value")
				
			else:
				if tokens[index+1] == "sys.input":
					variables[tokens[index-1]] = input(tokens[index+2])
					used_variable = True
					continue

				if tokens[index+1] == "sys.read":
					with open(tokens[index+2], "r") as sysread:
						variables[tokens[index-1]] = sysread.read()
						
					used_variable = True
					continue

				else:
					variables[tokens[index-1]] = tokens[index+1]
					used_variable = True

	# --// Compile Files

	for index, token in enumerate(tokens):
		if used_variable == True:
			used_variable = False
			continue
		
		if token == "sys.write":
			with open(tokens[index+1], "w") as syswrite:
				syswrite.write(tokens[index+2])

			used_variable = True
			
	# --// show parsed tokens

	print("Variable parse: ", tokens)
	print("Variable tree: ", variables)

	# --// Compile arguments

	for index, token in enumerate(tokens):
		if "(" in token and ")" in token and tokens[index-1] == "if":
			if_cache = []

			args = token.replace("(","").replace(")","").split(" ")

			if args[0] == "var":
				if variables[args[1]].replace('.','',1).isdigit():
					arg1 = float(variables[args[1]])
					
				else:
					arg1 = variables[args[1]]

				if args[3] == "var":
					if variables[args[4]].replace('.','',1).isdigit():
						arg2 = float(variables[args[4]])
						
					else:
						arg2 = variables[args[4]]
					
				else:
					if args[3].replace('.','',1).isdigit():
						arg2 = float(args[3])
						
					else:
						arg2 = args[3]

			else:
				if args[0].replace('.','',1).isdigit():
					arg1 = float(args[0])
					
				else:
					arg1 = args[0]

				if args[2] == "var":
					if variables[args[3]].replace('.','',1).isdigit():
						arg2 = float(variables[args[3]])
						
					else:
						arg2 = variables[args[3]]
		
				else:
					if args[2].replace('.','',1).isdigit():
						arg2 = float(args[2])
						
					else:
						arg2 = args[2]

			if args[0] == "var":
				expr = args[2]

			else:
				expr = args[1]
			
			for arg in tokens[index:]:
				if arg != "}":
					if_cache.append(arg)
				
				else:
					break

			if expr == "==":
				if arg1 == arg2:
					interperet(if_cache[2:])

			if expr == ">=":
				if arg1 >= arg2:
					interperet(if_cache[2:])
				
			if expr == "<=":
				if arg1 <= arg2:
					interperet(if_cache[2:])
				
			if expr == "!=":
				if arg1 != arg2:
					interperet(if_cache[2:])

	for index, token in enumerate(tokens):
		if "(" in token and ")" in token and tokens[index-2] == "func":
			func_name = tokens[index-1]
			
			func_tokens[func_name] = []
			func_tokens[func_name].append({})
			func_tokens[func_name][0]["args"] = []
			
			for arg in token[1:-1].split(","):
				if arg != "":
					func_tokens[func_name][0]["args"].append(arg)

	for index, token in enumerate(tokens):
		if "(" in token and ")" in token and tokens[index-2] == "loop":
			loop_name = tokens[index-1]
			
			loop_tokens[loop_name] = []
			loop_tokens[loop_name].append({})
			loop_tokens[loop_name][0]["args"] = []
			
			for arg in token[1:-1].split(","):
				if arg != "":
					loop_tokens[loop_name][0]["args"].append(arg)
					
	# --// Lexer

	for index, token in enumerate(tokens):
		if used_token == True:
			used_token = False
			continue
			
		if not index >= skip_index:
			continue
		
		if token == "print" and func == False:
			if tokens[index+1] == "sys.newline":
				print("\n")
				continue

			if tokens[index+1] == "sys.input":
				print(input(tokens[index+2]))
				used_token = True
				continue
			
			if tokens[index+1] == "var":
				print(variables[tokens[index+2]], end = '')
				skip_index = index + 2
				continue
			
			else:
				print(tokens[index+1])
				used_token = True
				continue

		if token == "func":
			if func == False:
				func = True
		
			else:
				print("[ Jade ] Cannot assign a function in a function")
		
			func_name = tokens[index+1]
			skip_index = index

			for findex, ftoken in enumerate(tokens[skip_index:]):
				if ftoken != func_name and ftoken != "func":
					func_tokens[func_name].append(ftoken)
					skip_index += 1

					if ftoken == "}":
						break
				
				else:
					continue
			
			skip_index = skip_index - 8
			pre_index = index
			func = False

			continue
		
		if token == "call":
			func_name = tokens[index+1]
			args = tokens[index+2]

			if len(args.split(",")) == len(func_tokens[func_name][0]["args"]):
				pass

			else:
				if func_tokens[func_name][0]["args"] != "()":
					pass

				else:
					print("[ Jade ] invalid function arguments: ", func_name)
					continue

			cargs = args.replace("(","").replace(")","").replace(" ","").split(",")

			#try:
			if True:
				for cfindex, cftoken in enumerate(cargs):
					if cftoken != "":
						variables[func_tokens[func_name][0]["args"][cfindex]] = cftoken

				if len(func_tokens[func_name]) > 0:
				
					for cindex, tok in enumerate(func_tokens[func_name]):
						#print(tok)
						if used_token == True:
							used_token = False
							
							continue
						
						if "print" in tok:
							if func_tokens[func_name][cindex+1] == "sys.newline":
								print("\n")
								continue
							
							if func_tokens[func_name][cindex+1] == "sys.input":
								print(input(func_tokens[func_name][cindex+2]))
								used_token = True
								continue
							
							if func_tokens[func_name][cindex+1] == "var":
								print(variables[func_tokens[func_name][cindex+2]], end = '')
							
							else:
								print(func_tokens[func_name][cindex+1], end = '')
								used_token = True

								
			#except Exception as e:
			#	print("invalid function arguments: {} | {}".format(func_name, e))
		
		if token == "loop":
			loop_name = tokens[index+1]
			lskip_index = index

			for findex, ftoken in enumerate(tokens[lskip_index:]):
				if ftoken != loop_name:
					loop_tokens[loop_name].append(ftoken)
					lskip_index += 1

					if ftoken == "}":
						break
				
				else:
					continue
			
			lskip_index = lskip_index - 8
			pre_index = index
			loop = False

			continue

		if token == "exec":
			used_token = True

			base_execute(tokens[index+1])
			continue
		
		if token == "run":
			loop_name = tokens[index+1]
			args = tokens[index+2]

			if len(args.split(",")) == len(loop_tokens[loop_name][0]["args"]):
				pass

			else:
				if loop_tokens[loop_name][0]["args"] != "()":
					pass

				else:
					print("[ Jade ] invalid function arguments: ", loop_name)
					continue

			cargs = args.replace("(","").replace(")","").replace(" ","").split(",")

			#try:
			if True:
				for lindex in range(int(cargs[0])):
		
					if len(loop_tokens[loop_name]) > 0:
					
						for cindex, tok in enumerate(loop_tokens[loop_name]):
							
							if used_token == True:
								used_token = False
								
								continue
							
							if "print" in tok:
								if loop_tokens[loop_name][cindex+1] == "sys.newline":
									print("\n")
									continue

								if loop_tokens[loop_name][cindex+1] == "sys.input":
									print(input(loop_tokens[loop_name][cindex+2]))
									used_token = True
									continue
								
								if loop_tokens[loop_name][cindex+1] == "var":
									print(variables[loop_tokens[loop_name][cindex+2]], end = '')
								
								else:
									print(loop_tokens[loop_name][cindex+1], end = '')
									used_token = True
								
			#except Exception as e:
			#	print("invalid loop arguments: {} | {}".format(loop_name, e))

	print(variables)
	print(func_tokens)
	print("\n\n\n")
	print(tokens)
