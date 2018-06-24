import os
import sys

DIR=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DIR, 'deps'))

import djangogo

parser=djangogo.make_parser()
args=parser.parse_args()
djangogo.main(args,
	project='scraper_proj',
	app='scraper',
	database='scraper_database',
	user='scraper_user',
	heroku_url='https://stark-mesa-98224.herokuapp.com/',
)
