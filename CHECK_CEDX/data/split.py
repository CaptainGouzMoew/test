import os
import pandas as pd

# Walk through all folders and subfolders starting from C:\
# for root, dirs, files in os.walk(r'C:\Users\BV053963\Desktop\PROJ\test\CHECK_CEDX\data\Bot_History_20231201_20231231_Part4\\'):
#     for file in files:
#         if file.endswith(".xlsx"):
#             path = os.path.join(root, file)
#             try:
#                 df = pd.read_excel(path, engine='openpyxl')
#                 df_new = df[:101]  # Take only the first 101 rows

#                 # Overwrite the same file
#                 df_new.to_excel(path, index=False)
#                 print(f'Processed: {path}')
#             except Exception as e:
#                 print(f'Error with file {path}: {e}')

for root, dirs, files in os.walk(r'C:\Users\BV053963\Desktop\PROJ\test\CHECK_CEDX\data\Bot_History_20231201_20231231_Part4\\'):
    # print(f'1. {root}\n,2. {dirs}\n, 3. {files}')
    for file in files:
        if file.endswith('.xlsx'):
            path = os.path.join(root, file)
            try:
                df = pd.read_excel(path)
                df_new = df[:101]

                df_new.to_excel(path, index= False)
                print(f'Finished {path}')
            except Exception as e:
                print(f'Err with {path}: {e}')
print('ok')




