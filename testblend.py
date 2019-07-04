import bge
import cv2 as cv
import datetime
#print(111)

scene = bge.logic.getCurrentScene()
o1 = scene.objects["a"]
o2 = scene.objects["b"]
sens = o1.sensors["Keyboard"]
#objlist = scene.objects
#print(objlist)
camera = scene.objects["Camera"]
text = scene.objects["Text"]
textHelp = scene.objects["TextHelp"]
#text.visible = False
if not hasattr(bge.logic, 'video_a'):
    #for o, im, v in [(o1, 'IMin1.png', '/home/student/trub-cv/img/out.avi'), (o2, 'IMin2.png', '/home/student/trub-cv/img/out2.avi')]:
    tex = bge.texture.materialID(o1, 'IMin1.png')
    bge.logic.video_a = bge.texture.Texture(o1, tex)
    textHelp.visible=False
    #bge.logic.video_a.source = bge.texture.VideoFFmpeg("0",0)
    bge.logic.video_a.source = bge.texture.VideoFFmpeg('/home/student/trub-cv/img/out_syn.avi')
    #bge.logic.video_a.source.scale = True
    #bge.logic.video_a.source.range = (5.,10.) # включить отрывок от а до b
    bge.logic.video_a.source.play()

if not hasattr(bge.logic, 'video_b'):
    #for o, im, v in [(o1, 'IMin1.png', '/home/student/trub-cv/img/out.avi'), (o2, 'IMin2.png', '/home/student/trub-cv/img/out2.avi')]:
    tex_b = bge.texture.materialID(o2, 'IMin2.png')
    bge.logic.video_b = bge.texture.Texture(o2, tex_b)
    #bge.logic.video_b.source = bge.texture.VideoFFmpeg("1",1)
    bge.logic.video_b.source = bge.texture.VideoFFmpeg('/home/student/trub-cv/img/out2_syn.avi')
    bge.logic.video_b.source.flip = False
    bge.logic.video_b.source.play()

#print(bge.logic.video_a.source.preseek) # 4TO ETO?
text.text = "t=%s\nh - помощь " % str(datetime.datetime.now().time())
textHelp.text = "WASD - передвижение\nSpace - пауза\nB - воспроизведение\nR - рестарт\nL"\
+" - ускорение\nK - обычная скорость\nLeftArrow - кручение сферы против\n"\
+"                  часовой стрелки\nRightArrow - по часовой\n"\
+"V - приближение"
bge.logic.video_a.refresh(True)
bge.logic.video_b.refresh(True)
for key,status in sens.events:
    if status == bge.logic.KX_INPUT_JUST_ACTIVATED:
        if key == bge.events.SPACEKEY: # key "spacebar" for pause
            bge.logic.video_a.source.pause()
            bge.logic.video_b.source.pause()
            textHelp.visible=False
        if key == bge.events.BKEY: # key "B" for unpause
            bge.logic.video_a.source.play()
            bge.logic.video_b.source.play()
            textHelp.visible=False
        if key == bge.events.RKEY: # key "r" for restart video
            bge.logic.video_a.source.stop()
            bge.logic.video_b.source.stop()
            bge.logic.video_a.source.play()
            bge.logic.video_b.source.play()
            textHelp.visible=False
        if key == bge.events.LKEY: # key ">" for upspeed video. every press the button +1 speed
            bge.logic.video_a.source.pause()
            bge.logic.video_b.source.pause()
            bge.logic.video_a.source.framerate += 1.
            bge.logic.video_b.source.framerate += 1.
            bge.logic.video_a.source.play()
            bge.logic.video_b.source.play()
            textHelp.visible=False
        if key == bge.events.KKEY: # key "<" for normal speed
            bge.logic.video_a.source.pause()
            bge.logic.video_b.source.pause()
            bge.logic.video_a.source.framerate = 1.
            bge.logic.video_b.source.framerate = 1.
            bge.logic.video_a.source.play()
            bge.logic.video_b.source.play()
            textHelp.visible=False
        if key == bge.events.HKEY: # key "h" for help
            if textHelp.get('helper') == True:
                textHelp.visible=False
                textHelp['helper'] = False
            else:
                textHelp.visible=True
                textHelp['helper'] = True
        if key == bge.events.VKEY:
            if 90 >= camera.fov > 25:
                camera.fov-=5
            else:
                camera.fov=90
            text.position[1] = 271.504/camera.fov + 0.29 #+ 6