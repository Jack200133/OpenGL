import pygame
from pygame.locals import *
from math import *
from shaders import *

from gl import Renderer, Model

width = 960
height = 540

deltaTime = 0.0

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)

rend.setShaders(vertex_shader, fragment_shader)

face = Model("model.obj","texture.bmp")

face.position.z -= 3
face.position.y -= 3
face.scale.x = 0.01
face.scale.y = 0.01
face.scale.z = 0.01
rend.target = face.position
rend.scene.append( face )


isRunning = True

while isRunning:

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            elif event.key == pygame.K_1:
                rend.filledMode()
            elif event.key == pygame.K_2:
                rend.wireframeMode()

        if event.type == pygame.MOUSEWHEEL:
            rend.camPosition.z += event.y


    if keys[K_a]:
        rend.angle -= 30 *deltaTime

    elif keys[K_d]:
        rend.angle += 30 *deltaTime

    if keys[K_w]:
        if rend.camDistance < 10:
            rend.camPosition.y += 5 * deltaTime

    elif keys[K_s]:
        if rend.camDistance > -10:
            rend.camPosition.y -= 5 * deltaTime
    if keys[K_LEFT]:
        rend.pointLight.x += 10 * deltaTime

    elif keys[K_RIGHT]:
        rend.pointLight.x -= 10 * deltaTime

    if keys[K_UP]:
        rend.pointLight.y -= 10 * deltaTime

    elif keys[K_DOWN]:
        rend.pointLight.y += 10 * deltaTime

    elif keys[K_l]:
        if rend.camDistance < 10:
            rend.camDistance += 5 * deltaTime

    elif keys[K_k]:
        if rend.camDistance > 3:
            rend.camDistance -= 5 * deltaTime

    rend.target.y = rend.camPosition.y

    rend.target.x = rend.camPosition.x + sin(radians(rend.angle)) * rend.camDistance
    rend.target.z = rend.camPosition.z + cos(radians(rend.angle)) * rend.camDistance
    
    deltaTime = clock.tick(60) / 1000
    rend.time += deltaTime
    #print(deltaTime)

    rend.update()
    rend.render()
    pygame.display.flip()

pygame.quit()
