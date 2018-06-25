import os
import sys

DIR=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DIR, 'deps'))

import djangogo

parser=djangogo.make_parser()
parser.add_argument('--start-scheduler', action='store_true', help='start scraper scheduler')
args=parser.parse_args()

if args.start_scheduler:
	djangogo.invoke('heroku', 'ps:scale', 'scheduler=1')

djangogo.main(args,
	project='scraper_proj',
	app='scraper',
	database='scraper_database',
	user='scraper_user',
	heroku_url='https://stark-mesa-98224.herokuapp.com/',
)
