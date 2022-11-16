from pickle import TRUE
import pygame
from pygame.locals import *

from shaders import *

from gl import Renderer, Model

from math import cos, sin, radians

width = 960
height = 540

deltaTime = 0.0

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)

rend.setShaders(vertex_shader, fragment_shader)

rend.target.z = -5

face = Model("nave/model.obj", "nave/texture.bmp")
ufos = Model("ufo/model.obj", "ufo/texture.bmp")
raven = Model("raven/model.obj", "raven/texture.bmp")
ship = Model("ship/model.obj", "ship/texture.png")
imperial = Model("imperial/model.obj", "imperial/texture.jpeg")

face.position.z -= 5
face.scale.x = 0.01
face.scale.y = 0.01
face.scale.z = 0.01

ufos.position.z -= 5

raven.position.z -= 5
raven.scale.x = 0.005
raven.scale.y = 0.005
raven.scale.z = 0.005

ship.position.z -= 5
ship.scale.x = 0.5
ship.scale.y = 0.5
ship.scale.z = 0.5

imperial.position.z -= 5
imperial.scale.x = 0.005
imperial.scale.y = 0.005
imperial.scale.z = 0.005


rend.scene.append( face )


isRunning = True

while isRunning:

    keys = pygame.key.get_pressed()
    rend.timestamp.x += deltaTime

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        elif event.type == pygame.MOUSEMOTION:
            position = pygame.mouse.get_pos()
            rend.angle = (position[0] - width/2) 
            rend.camPosition.y = (position[1] - height/2)/100

        elif event.type == pygame.MOUSEWHEEL:
            if event.y  > 0:
                if rend.camDistance > 2:
                    rend.camDistance -= event.y
            else:
                if rend.camDistance <10:
                    rend.camDistance -= event.y
            

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

            elif event.key == pygame.K_z:
                rend.filledMode()
            elif event.key == pygame.K_x:
                rend.wireframeMode()
            elif event.key == pygame.K_1:
                rend.setShaders(vertex_shader, fragment_shader)
            elif event.key == pygame.K_2:
                rend.setShaders(vertex_shader, toon_shader)
            elif event.key == pygame.K_3:
                rend.setShaders(vertex_shader, rainbow_shader)
            elif event.key == pygame.K_4:
                rend.setShaders(vertex_shader, siren_shader)
            elif event.key == pygame.K_5:
                rend.setShaders(gomu_gomu_shader, fragment_shader)
            elif event.key == pygame.K_6:
                rend.scene.clear()
                rend.scene.append( face )
            elif event.key == pygame.K_7:
                rend.scene.clear()
                rend.scene.append( ufos )
            elif event.key == pygame.K_8:
                rend.scene.clear()
                rend.scene.append( raven )
            elif event.key == pygame.K_9:
                rend.scene.clear()
                rend.scene.append( ship )
            elif event.key == pygame.K_0:
                rend.scene.clear()
                rend.scene.append( imperial )


    if keys[K_q]:
        if rend.camDistance > 2:
            rend.camDistance -= 2 * deltaTime
    elif keys[K_e]:
        if rend.camDistance < 10:
            rend.camDistance += 2 * deltaTime
    elif keys[K_f]:
        rend.colorRaibow.x += 1 * deltaTime

    if keys[K_a]:
        rend.angle -= 30 * deltaTime
    elif keys[K_d]:
        rend.angle += 30 * deltaTime


    if keys[K_w]:
        #if rend.camPosition.y < 2:
        rend.camPosition.y += 5 * deltaTime
    elif keys[K_s]:
        #if rend.camPosition.y > -2:
        rend.camPosition.y -= 5 * deltaTime


    #rend.target.y = rend.camPosition.y

    rend.camPosition.x = rend.target.x + sin(radians(rend.angle)) * rend.camDistance
    rend.camPosition.z = rend.target.z + cos(radians(rend.angle)) * rend.camDistance
    
    if keys[K_LEFT]:
        rend.pointLight.x -= 10 * deltaTime
    elif keys[K_RIGHT]:
        rend.pointLight.x += 10 * deltaTime
    elif keys[K_UP]:
        rend.pointLight.y += 10 * deltaTime
    elif keys[K_DOWN]:
        rend.pointLight.y -= 10 * deltaTime


    deltaTime = clock.tick(60) / 1000
    rend.time += deltaTime

    rend.update()
    rend.render()
    pygame.display.flip()

pygame.quit()
