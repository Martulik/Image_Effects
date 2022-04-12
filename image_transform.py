import os
import ffmpeg

(w,h) = (640,640)
clip_len = 12

def blurOut():
    filtersBlurOut = [
        f"[1]split[orig][blur]",
        f"[blur]avgblur=sizeX=130:sizeY=20,fade=t=in:st=0:d={clip_len}:alpha=1[blur]",
        f"[orig]fade=t=out:st=0:d={clip_len}[orig]",
        f"[orig][blur]overlay"
    ]
    filters = ",".join(filtersBlurOut)
    return filters

def blurIn():
    filtersBlurIn = [
        f"[1]split[orig][blur]",
        f"[blur]avgblur=sizeX=130:sizeY=20,fade=t=out:st=0:d={clip_len}:alpha=1[blur]",
        f"[orig]fade=t=in:st=0:d={clip_len}[orig]",
        f"[orig][blur]overlay"
    ]
    filters = ",".join(filtersBlurIn)
    return filters

def dark():
    filterDark = []
    filterDark.append(f"[1]scale={w}:-1,split[x11][x12]")
    filterDark.append(f"[x11]fade=t=in:st=0:d=12[x21],[0][x21]overlay=(W-w)/2:(H-h)/2,trim=0:12[b1]")
    filterDark.append(f"[x12]fade=t=out:st=0:d=12[x22],[0][x22]overlay=(W-w)/2:(H-h)/2,trim=0:12[b2]")
    filterDark.append("[b1][b2]concat")
    filters = ",".join(filterDark)
    return filters

def scroll():
    filterTest = [
        f"[1:v]scale=960:0[fg], [0:v][fg]overlay=y=-'t*((h-1080)/5)':eof_action=endall"
    ]
    filters = ",".join(filterTest)
    return filters

def scale():
    filterTest = [
        #f"[0:v]scale=8000x4000,zoompan=z='min(zoom+0.0015,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=125"
        f"scale=iw*4:ih*4,zoompan=z='if(lte(mod(on,60),30),zoom+0.002,zoom-0.002)':x='iw/2-(iw/zoom)/2':y='ih/2-(ih/zoom)/2':d=25*5"
    ]
    filters = ",".join(filterTest)
    return filters

######


input_file = input("Enter the name of input file : ")
if not os.path.isfile(input_file):
    print (f"File {input_file} not exist")
    exit()
 


print("Enter a number to select the effect")
print("1 - blur out")
print("2 - blur in")
print("3 - gradual darkening")
print("4 - scrolling")
print("5 - scale")

command_str = input("Enter comand : ")
command = int(command_str)

cmd = f"ffmpeg "
if command != 5:
    cmd += f"-f lavfi -i color=c=gray:s={w}x{h} "
cmd += f"-loop 1 -i {input_file} "

out_file = input("Enter the name of output file : ")
if command == 1:
    cmd += f"-filter_complex \"{blurOut()}\" "
elif command == 2:
    cmd += f"-filter_complex \"{blurIn()}\" "
elif command == 3:
    cmd += f"-filter_complex \"{dark()}\" "
    clip_len = clip_len * 2
elif command == 4:
    cmd += f"-filter_complex \"{scroll()}\" "
    clip_len = clip_len / 2
elif command == 5:
    cmd += f"-vf \"{scale()}\" "
    cmd += f"-c:v libx264 -t {clip_len} -s \"1280x720\" {out_file} -y"
    print(cmd)
    os.system(cmd)
    exit()
else:
    print("wrong command")
    exit

cmd += f"-t {clip_len} "
cmd += f"-y {out_file}"
 
print(cmd)
os.system(cmd)
os.system(r'"/Applications/VLC.app" ' + out_file)
