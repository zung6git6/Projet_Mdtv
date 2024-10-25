import re
in_file = 'annule_arg.TS'
out_file = 'annule_arg_parse.log'
all_parse_states = [ 'P0' ]
terminals_re = { '#'      : '^[ \n]*#[ \n]*' ,
                 '}'      : '^[ \n]*}[ \n]*' ,
                 'I'      : '^[ \n]*I[ \n]*' ,
                 'P'      : '^[ \n]*P[ \n]*' ,
                 'G'      : '^[ \n]*G[ \n]*' ,
                 'D'      : '^[ \n]*D[ \n]*' ,
                 '0'      : '^[ \n]*0[ \n]*' ,
                 '1'      : '^[ \n]*1[ \n]*' ,
                 'fin'    : '^[ \n]*fin[ \n]*' ,
                 'boucle' : '^[ \n]*boucle[ \n]*' ,
                 'si(0)'  : '^[ \n]*si[ \n]*\([ \n]*0[ \n]*\)[ \n]*' ,
                 'si(1)'  : '^[ \n]*si[ \n]*\([ \n]*1[ \n]*\)[ \n]*' }

terminals_automata = { x : re.compile( terminals_re[ x ] ) for x in terminals_re.keys() }

def tokenize( in_f, terms_autom = {} ):
     txt = in_f.read()
     txt_sz = len( txt )
     tokens = []
     match = True
     while match and (len( txt ) != 0):
          for tok_nm in terms_autom.keys():
               #print( 'begining of text == ', txt[ 0 : min(10, len( txt )) ] )
               #print( '\t searching for token ', tok_nm )
               match = terms_autom[ tok_nm ].search( txt )
               if match:
                    #print( 'match found ' , match )
                    (b, e ) = match.span( 0 )
                    #print( '-------> ', (b, e ) )
                    if b == 0:
                         tokens.append( tok_nm )
                         txt = txt[ e: ]
                         break
               else:
                    #print( tok_nm + ' match failed' )
                    pass
     #print( tokens )
     if match or len( txt ) == 0:
          return tokens
     else:
          print( 'ERROR unknow token encountered in the input at position {0}'.format( txt_sz - len( txt ) ) )
          print( 'aborting' )
          exit( 1 )

def next_tok( tokens ):
     if tokens == []:
          print( 'ERROR in next_tok() no token available}')
          return ''
     else:
      return tokens[ 0 ]


def main_parse( terms_autom ):
     with open( in_file, 'rt') as in_fdesc:
          with open( out_file, 'wt' ) as out_fdesc:
               tokens = tokenize( in_fdesc, terms_autom )
               return P0( tokens, out_fdesc )
          

def P0( tokens, out_f, parse_state = 'P0', K = 0 ):
     tok = next_tok( tokens )
     # out_f.write( 'in state {0} with new input token {1} and K == {2}\n'.format( parse_state, tok, K ))
     if ( tok == '#') and (K == 0):
          out_f.write( tok + '\n' )
          return True
     elif tok in [ 'I', 'P', 'G', 'D', '0', '1', 'fin' ]:
          out_f.write( tok + '\n' )
          return P0( tokens[ 1: ], out_f, 'P0', K )
     elif tok in [ 'boucle', 'si(0)', 'si(1)' ]:
          out_f.write( tok + '\n' )
          return P0( tokens[ 1: ], out_f, 'P0', K + 1 )
     elif tok == '}':
          if K < 1:
               print( 'ERROR unbalanced closing code block token "}"' )
               return False
          else:
               out_f.write( tok + '\n' )
               return P0( tokens[ 1: ], out_f, 'P0', K - 1 )
     else:
          print( 'ERROR unexpected end of input' )
          return False

main_parse( terminals_automata )
