import datetime
import os

import common
import settings

settings.DEBUG = False


if __name__ == "__main__":

	with open('email_template.html') as f:
		template = f.read()

	outdir = "out-{}".format(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
	os.mkdir(outdir)

	users = common.get_domain_users()
	for user in users:
		user_email = user['primaryEmail']
		user_name = user['name'].get('givenName', user_email)

		print("\n{}:".format(user_email))
		public_files = common.get_publicly_shared_files(user_email)

		if public_files:
			result_elem = ""
			for file in public_files:
				print("    {}".format(file['name']))
				result_elem += "<li><a href=\"{link}\">{name}</a></li>\n".format(link=file['webViewLink'], name=file['name'])
			output = template.format(name=user_name, result_elem=result_elem, email=user_email)

			with open("{}/{}.html".format(outdir, user_email), "w") as outfile:
				outfile.write(output)
	print("\ndone.")
