import asyncio
import email
import imaplib

EMAIL = 'vezz@tyreat.com'
PASSWORD = 'Balikpapan1'
SERVER = 'tyreat.com'


def get_akun():
    with open('email.txt', 'r') as f:
        for line in f:
            if line.strip() == '':
                continue

            line = line.split('|')
            email = line[0]
            password = line[1]
            server = line[2]

            yield {
                'email': email,
                'password': password,
                'server': server
            }



async def get_email(emailacc, password, server):
    print('connect')
    mail = imaplib.IMAP4(server)
    mail.login(emailacc, password)
    mail.select('inbox')

    status, data = mail.search(None, 'ALL')
    mail_ids = []

    for block in data:
        mail_ids += block.split()

    for i in mail_ids:
        status, data = mail.fetch(i, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                
                message = email.message_from_bytes(response_part[1])

                mail_from = message['from']
                mail_subject = message['subject']

                
                if message.is_multipart():
                    mail_content = ''
                    for part in message.get_payload():
                        # if the content type is text/plain
                        # we extract it
                        if part.get_content_type() == 'text/plain':
                            mail_content += part.get_payload()
                else:
                    # if the message isn't multipart, just extract it
                    mail_content = message.get_payload()

                # and then let's show its result
                print(f'From: {mail_from}')
                print(f'Subject: {mail_subject}')
                print(f'Content: {mail_content}')

async def run():
    tasks = []
    for data in get_akun():
        tasks.append(get_email(data['email'], data['password'], data['server']))
        tasks.append(get_email(data['email'], data['password'], data['server']))
        tasks.append(get_email(data['email'], data['password'], data['server']))

    await asyncio.gather(*tasks)


asyncio.run(run())