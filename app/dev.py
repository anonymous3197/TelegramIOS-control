from os.path import dirname,join
curdir = dirname(__file__)
root_path = dirname(curdir)
backup_path = join(root_path,'BackupData')
print(backup_path)

        # app = ATT_DAV(ip)
        # results = app.client.list()
        # for result in results:
        #     if 'TelegramCS' in result:
        #         data_folder = result + 'data'
        #         local_path = join(curdir,'BackupData',f'data_{ip}/{data_folder}')