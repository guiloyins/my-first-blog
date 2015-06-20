nome1='Angela'
nome2='Paulo'
nome3='Julia'
nome4='Bernardo'
nome5='Patrick'
def hi(name):

	if name=='nome1':
		print('Hey, {nome1}!'.format(nome1=nome1,nome2=nome2,nome3=nome3,nome4=nome4,nome5=nome5))
	elif name=='nome2':
		print('Hey, {nome2}!'.format(nome1=nome1,nome2=nome2,nome3=nome3,nome4=nome4,nome5=nome5))
	elif name=='nome3':
		print('Hey, {nome3}!'.format(nome1=nome1,nome2=nome2,nome3=nome3,nome4=nome4,nome5=nome5))
	elif name=='nome4':
		print('Hey, {nome4}!'.format(nome1=nome1,nome2=nome2,nome3=nome3,nome4=nome4,nome5=nome5))
	elif name=='nome5':
		print('Hey, {nome5}!'.format(nome1=nome1,nome2=nome2,nome3=nome3,nome4=nome4,nome5=nome5))
	else:
		print('Hey, esquisito!')

hi('nome5')