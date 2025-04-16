from settings import *
import math
from entity import BaseEntity
from bullet import Bullet
from itertools import cycle


class Player(BaseEntity):
    def __init__(self, app, name='player'):
        super().__init__(app, name)
        self.group.change_layer(self, CENTER.y)

        self.rect = self.image.get_rect(center=CENTER)

        self.offset = vec2(0)
        self.inc = vec2(0)
        self.prev_inc = vec2(0)
        self.angle = 0
        self.diag_move_corr = 1 / math.sqrt(2)

        self.down_ind = [ 0, 1, 2, 3, 4]
        self.down_list = cycle( self.down_ind )
        self.up_ind = [ 0, 1, 2, 3, 4]
        self.up_list = cycle( self.up_ind )
        self.left_ind = [ 0, 1, 2, 3, 4]
        self.left_list = cycle( self.left_ind )
        self.right_ind = [ 0, 1, 2, 3, 4]
        self.right_list = cycle( self.right_ind )

        self.direction = 'DOWN'
        self.moving = False



    def control(self):
        self.moving = False
        self.inc = vec2(0)
        speed = PLAYER_SPEED * self.app.delta_time
        rot_speed = PLAYER_ROT_SPEED * self.app.delta_time

        key_state = pg.key.get_pressed()

        if key_state[pg.K_LEFT]:
            self.angle += rot_speed
        if key_state[pg.K_RIGHT]:
            self.angle -= rot_speed

        if key_state[pg.K_w]:
            self.inc += vec2(0, -speed).rotate_rad(-self.angle)
            self.direction = 'UP'
            self.moving = True
        if key_state[pg.K_s]:
            self.inc += vec2(0, speed).rotate_rad(-self.angle)
            self.direction = 'DOWN'
            self.moving = True
        if key_state[pg.K_a]:
            self.inc += vec2(-speed, 0).rotate_rad(-self.angle)
            self.direction = 'LEFT'
            self.moving = True
        if key_state[pg.K_d]:
            self.inc += vec2(speed, 0).rotate_rad(-self.angle)
            self.direction = 'RIGHT'
            self.moving = True

        if self.inc.x and self.inc.y:
            self.inc *= self.diag_move_corr

    def single_fire(self, event):
        if event.key == pg.K_UP:
            Bullet(app=self.app)

    def check_collision(self):
        hitobst = pg.sprite.spritecollide(self, self.app.collision_group,
                                      dokill=False, collided=pg.sprite.collide_mask)
        hit = pg.sprite.spritecollide(self, self.app.entity_group,
                                      dokill=False, collided=pg.sprite.collide_mask)
        if not hitobst and not hit:
            if self.inc.x or self.inc.y:
                self.prev_inc = self.inc
        else:
            self.inc = -self.prev_inc
            if hit:
                try:
                    self.app.message.set_message(hit[0].message)
                    self.app.message.active = True
                except AttributeError:
                    pass

                
    def animate(self):
        if self.app.anim_trigger:
            if self.direction == 'DOWN':
                if self.moving:
                    self.frame_index = next( self.down_list )
                else:
                    self.frame_index = self.down_ind[ 1 ]
            elif self.direction == 'UP':
                if self.moving:
                    self.frame_index = next( self.up_list )
                else:
                    self.frame_index = self.up_ind[ 1 ]
            elif self.direction == 'LEFT':
                if self.moving:
                    self.frame_index = next( self.left_list )
                else:
                    self.frame_index = self.left_ind[ 1 ]
            else:
                if self.moving:
                    self.frame_index = next( self.right_list )
                else:
                    self.frame_index = self.right_ind[ 1 ]



            self.image = self.images[self.frame_index]


    def update(self):
        #super().update() 
        self.animate()
        self.control()
        self.check_collision()
        self.move()

    def move(self):
        self.offset += self.inc
















