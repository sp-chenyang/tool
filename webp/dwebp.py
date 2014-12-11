# Decompress a WebP file to an image file, from google.
DWEBP = "E:\\opt\\libwebp-0.4.2-windows-x64\\bin\\dwebp.exe"

import os
cmd = DWEBP + ' test.webp -o test.png'
print os.system(cmd) # returns the exit status
