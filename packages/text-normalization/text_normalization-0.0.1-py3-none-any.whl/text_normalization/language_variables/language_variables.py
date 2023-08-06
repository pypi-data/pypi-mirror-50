regex_portuguese = r'\b[a-zA-ZãáàâçéêíõóôúüÃÁÀÂÇÉÊÍÕÓÔÚÜ’“«–,<<().?!][a-zA-ZãáàâçéêíõóôúüÃÁÀÂÇÉÊÍÕÓÔÚÜ-]*[a-zA-ZãáàâçéêíõóôúüÃÁÀÂÇÉÊÍÕÓÔÚÜ’”»>>)…–$%€.!?]*\b'

regex_french = r'\b[a-zA-ZãáàâçéêëíïõóôúüûùÃÁÀÂÇÉÊÍÕÓÔÚÜ’“«–,<<().?!][a-zA-ZãáàâçéêëïíõóôúüûùÃÁÀÂÇÉÊÍÕÓÔÚÜ-]*[a-zA-ZãáàâçéêëïíõóôúüûùÃÁÀÂÇÉÊÍÕÓÔÚÜ’”»>>)…–$%€.!?]*\b'

regex_english = r'\b[a-zA-Z’“«–,<<().!?][a-zA-Z-]*[a-zA-Z’”»>>)…–$%€.?!]*\b'

regex_spanish = r'\b[a-zA-ZãáàâçéêëíïõóôúüûùñÃÁÀÂÇÉÊÍÕÓÔÚÜ’“¿¡«–,<<()!.?][a-zA-ZãáàâçéêëïíõóôúüûùñÃÁÀÂÇÉÊÍÕÓÔÚÜ-]*[a-zA-ZãáàâçéêëïíõóôúüûùñÃÁÀÂÇÉÊÍÕÓÔÚÜ’”»>>)…–$%€¿¡.?!]*\b'

regex_word = {  'pt' : regex_portuguese,
                    'fr' : regex_french,
                    'en' : regex_english,
                    'es' : regex_spanish
                    }

percentage = {  'pt' : ' por cento ',
                'fr' : ' pour cent ',
                'en' : ' per cent ',
                'es' : ' por ciento '
            }

slash = {       'pt' : ' por ',
                'fr' : ' pour ',
                'en' : ' per ',
                'es' : ' por '
            }

months_portuguese = {'01': 'janeiro',
                     '02': 'fevereiro',
                     '03': 'março',
                     '04': 'abril',
                     '05': 'maio',
                     '06': 'junho',
                     '07': 'julho',
                     '08': 'agosto',
                     '09': 'setembro',
                     '10': 'outubro',
                     '11': 'novembro',
                     '12': 'dezembro'
                     }

months_french = {'01': 'janvier',
                 '02': 'février',
                 '03': 'mars',
                 '04': 'avril',
                 '05': 'mai',
                 '06': 'juin',
                 '07': 'juillet',
                 '08': 'août',
                 '09': 'septembre',
                 '10': 'octobre',
                 '11': 'novembre',
                 '12': 'décembre'
                 }

months_english = {'01': 'january',
                  '02': 'february',
                  '03': 'march',
                  '04': 'april',
                  '05': 'may',
                  '06': 'june',
                  '07': 'july',
                  '08': 'august',
                  '09': 'september',
                  '10': 'october',
                  '11': 'november',
                  '12': 'december'
                  }

months_spanish = {'01': 'enero',
                  '02': 'febrero',
                  '03': 'marzo',
                  '04': 'abril',
                  '05': 'mayo',
                  '06': 'junio',
                  '07': 'julio',
                  '08': 'agosto',
                  '09': 'septiembre',
                  '10': 'octubre',
                  '11': 'noviembre',
                  '12': 'deciembre'
                  }

months_all = {'pt': months_portuguese,
              'fr': months_french,
              'en': months_english,
              'es': months_spanish
              }
