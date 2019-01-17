import json
import os
import sys
import subprocess
from datetime import datetime

def run_command(full_command):
    proc = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    try:
        output = proc.communicate()
    except:
        pass
    return b''.join(output).strip().decode()  # only save stdout into output, ignore stderr


def delete_tags(expiration_image_list):
    for image in expiration_image_list:
        name = image['name']
        id = image['id']
        created_date = image['created']
        dte = int(image['annotations']['DTE'])
        tag = image['tag']
        
        format_str = '%Y-%m-%dT%H:%M:%S.%fZ'

        date = datetime.strptime(created_date, format_str)

        todays_date = (datetime.now())

        if tag != '<none>':

            days_alive = (todays_date - date).days

            days_left = dte - days_alive

            if days_left <= 0:
                print('Untagging Image: {} ID: {} Tag: {}'.format(name, id, tag))
                run_command('codefresh untag {} {}'.format(id, tag))
            else:
                print('Scheduled in {} Day(s) -- Image: {} ID: {} Tag: {} '.format(str(days_left), name, id, tag))


def main():

    # Get list of expiration images
    raw_json = run_command('codefresh get image --label EXPIRATION=true -o json')
    expiration_image_list = json.loads(raw_json)

    # Untag images past their expiration date
    delete_tags(expiration_image_list)

if __name__ == "__main__":
    main()
