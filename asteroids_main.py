import pygame
import random
import math
import uuid

# global variables
screen_width = 1200
screen_height = 660
BLACK = (0, 0, 0)

# mass and velocity range properties
big_meteor_properties = [100, [3, 8]]
med_meteor_properties = [40, [5, 10]]
small_meteor_properties = [15, [7, 12]]
tiny_meteor_properties = [5, [9, 15]]

# dictionary of the meteor properties and their corresponding image files
types_meteor_dict = {1: [big_meteor_properties, [pygame.image.load("meteorBrown_big1.png"), pygame.image.load("meteorBrown_big2.png"), pygame.image.load("meteorBrown_big3.png"), pygame.image.load("meteorBrown_big4.png")]],
                     2: [med_meteor_properties, [pygame.image.load("meteorBrown_med1.png")]],
                     3: [small_meteor_properties, [pygame.image.load("meteorBrown_small1.png")]],
                     4: [tiny_meteor_properties, [pygame.image.load("meteorBrown_tiny1.png")]]}

# dictionary to contain the grid subspaces as keys and they contain the meteorite objects
# keys format [x1, x2, y1, y2] x1-x2 grid and y1-y2 grid
grid_subspaces = {}
for i in range(0, screen_width, 100):
    for j in range(0, screen_height, 60):
        grid_subspaces[str(i) + "," + str(i+100) + "," + str(j) + "," + str(j+60)] = {}

# player information
player_file_name = "playerShip1_blue.png"


class Player(pygame.sprite.Sprite):
    def __init__(self, img_file):
        pygame.sprite.Sprite.__init__(self)
        self.player_dimension = (40, 40)
        self.angle = 0
        self.image = pygame.transform.scale(pygame.image.load(img_file), self.player_dimension)
        self.image.set_colorkey((0, 0, 0))
        self.image_convert = self.image.convert()
        self.xpos = 0
        self.ypos = 0
        self.stepx = 10
        self.stepy = 10
        self.health = 1000
        self.gridx1 = 0
        self.gridx2 = 0
        self.gridy1 = 0
        self.gridy2 = 0
        self.current_key = ""
        self.width = pygame.transform.rotate(self.image_convert, self.angle).get_width()
        self.height = pygame.transform.rotate(self.image_convert, self.angle).get_height()

    def get_rect(self):
        return pygame.Rect(self.xpos, self.ypos, self.width, self.height)

    def movement(self):
        change_x = math.sin(self.angle*math.pi/180)*self.stepx
        change_y = math.cos(self.angle*math.pi/180)*self.stepx
        if change_x > 0 and self.xpos - self.player_dimension[0] > 0:
            self.xpos -= change_x
        if change_x < 0 and self.xpos + self.player_dimension[0] < screen_width:
            self.xpos -= change_x
        if change_y > 0 and self.ypos - self.player_dimension[0] > 0:
            self.ypos -= change_y
        if change_y < 0 and self.ypos + self.player_dimension[0] < screen_height:
            self.ypos -= change_y

    def update_grid(self):
        player_prev_key_name = self.current_key
        # input into grid based on center of image, not the xpos/ypos
        img_width = self.image.get_width()
        img_height = self.image.get_height()
        x_grid_1 = round(((self.xpos + round(img_width // 2)) // 100) * 100)
        y_grid_1 = round(((self.ypos + round(img_height // 2)) // 60) * 60)

        x_grid_2 = x_grid_1 + 100
        y_grid_2 = y_grid_1 + 60
        key_name = str(x_grid_1) + "," + str(x_grid_2) + "," + str(y_grid_1) + "," + str(y_grid_2)

        self.gridx1 = x_grid_1
        self.gridx2 = x_grid_2
        self.gridy1 = y_grid_1
        self.gridy2 = y_grid_2

        self.current_key = key_name
        player_new_key_name = self.current_key
        if player_prev_key_name != player_new_key_name:
            if player_prev_key_name in grid_subspaces:
                grid_subspaces[player_prev_key_name].pop(self)

            if player_new_key_name in grid_subspaces:
                grid_subspaces[player_new_key_name][self] = 1
        return key_name

    def check_proximity(self):
        # get a list of meteorites in the surrounding grids a total of 9 grids 3x3 with center being the self meteor
        meteorites_list = []

        # keys of the surrounding grids 9 in total, 3x3
        keyname_1 = str(self.gridx1 - 100) + "," + str(self.gridx2 - 100) + "," + str(self.gridy1 - 60) + "," + str(
            self.gridy2 - 60)
        keyname_2 = str(self.gridx1) + "," + str(self.gridx2) + "," + str(self.gridy1 - 60) + "," + str(
            self.gridy2 - 60)
        keyname_3 = str(self.gridx1 + 100) + "," + str(self.gridx2 + 100) + "," + str(self.gridy1 - 60) + "," + str(
            self.gridy2 - 60)
        keyname_4 = str(self.gridx1 - 100) + "," + str(self.gridx2 - 100) + "," + str(self.gridy1) + "," + str(
            self.gridy2)
        keyname_5 = self.current_key
        keyname_6 = str(self.gridx1 + 100) + "," + str(self.gridx2 + 100) + "," + str(self.gridy1) + "," + str(
            self.gridy2)
        keyname_7 = str(self.gridx1 - 100) + "," + str(self.gridx2 - 100) + "," + str(self.gridy1 + 60) + "," + str(
            self.gridy2 + 60)
        keyname_8 = str(self.gridx1) + "," + str(self.gridx2) + "," + str(self.gridy1 + 60) + "," + str(
            self.gridy2 + 60)
        keyname_9 = str(self.gridx1 + 100) + "," + str(self.gridx2 + 100) + "," + str(self.gridy1 + 60) + "," + str(
            self.gridy2 + 60)

        all_keys = [keyname_1, keyname_2, keyname_3, keyname_4, keyname_5, keyname_6, keyname_7, keyname_8, keyname_9]

        # checks if the key exist in the grid_subspaces, if the exist, append to meteorites_list the meteor objects
        for i in all_keys:
            if i in grid_subspaces:
                for meteor in grid_subspaces[i]:
                    if type(meteor) != Player and type(meteor) != Bullets:
                        meteorites_list.append(meteor)
        return meteorites_list

    def draw(self, win):
        player_image_copy = pygame.transform.rotate(self.image_convert, self.angle)
        win.blit(player_image_copy, (self.xpos - int(player_image_copy.get_width() / 2), self.ypos - int(player_image_copy.get_width() / 2)))


class Bullets:
    def __init__(self, xpos, ypos, angle):
        self.bullet_dimension = (10, 10)
        self.image = pygame.transform.scale(pygame.image.load("bullet_asteroid.png").convert_alpha(), self.bullet_dimension)
        self.xpos = xpos
        self.ypos = ypos
        self.velocity = 10
        self.angle = angle
        self.current_key = ""
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.gridx1 = 0
        self.gridx2 = 0
        self.gridy1 = 0
        self.gridy2 = 0

    def get_rect(self):
        return pygame.Rect(self.xpos, self.ypos, self.width, self.height)

    def movement(self):
        change_x = math.sin(self.angle*math.pi/180)*self.velocity
        change_y = math.cos(self.angle*math.pi/180)*self.velocity
        self.xpos -= change_x
        self.ypos -= change_y

    def update_grid(self):
        bullet_key = self.current_key
        # input into grid based on center of image, not the xpos/ypos
        x_grid_1 = round(((self.xpos + round(self.width // 2)) // 100) * 100)
        y_grid_1 = round(((self.ypos + round(self.height // 2)) // 60) * 60)

        x_grid_2 = x_grid_1 + 100
        y_grid_2 = y_grid_1 + 60
        key_name = str(x_grid_1) + "," + str(x_grid_2) + "," + str(y_grid_1) + "," + str(y_grid_2)

        self.gridx1 = x_grid_1
        self.gridx2 = x_grid_2
        self.gridy1 = y_grid_1
        self.gridy2 = y_grid_2

        self.current_key = key_name
        new_bullet_key = self.current_key
        if bullet_key != new_bullet_key:
            if bullet_key in grid_subspaces:
                grid_subspaces[bullet_key].pop(self)

            if new_bullet_key in grid_subspaces:
                grid_subspaces[new_bullet_key][self] = 1

        return key_name

    def check_proximity(self):
        # get a list of meteorites in the surrounding grids a total of 9 grids 3x3
        meteorites_list = []

        # keys of the surrounding grids 9 in total, 3x3
        keyname_1 = str(self.gridx1 - 100) + "," + str(self.gridx2 - 100) + "," + str(self.gridy1 - 60) + "," + str(
            self.gridy2 - 60)
        keyname_2 = str(self.gridx1) + "," + str(self.gridx2) + "," + str(self.gridy1 - 60) + "," + str(
            self.gridy2 - 60)
        keyname_3 = str(self.gridx1 + 100) + "," + str(self.gridx2 + 100) + "," + str(self.gridy1 - 60) + "," + str(
            self.gridy2 - 60)
        keyname_4 = str(self.gridx1 - 100) + "," + str(self.gridx2 - 100) + "," + str(self.gridy1) + "," + str(
            self.gridy2)
        keyname_5 = self.current_key
        keyname_6 = str(self.gridx1 + 100) + "," + str(self.gridx2 + 100) + "," + str(self.gridy1) + "," + str(
            self.gridy2)
        keyname_7 = str(self.gridx1 - 100) + "," + str(self.gridx2 - 100) + "," + str(self.gridy1 + 60) + "," + str(
            self.gridy2 + 60)
        keyname_8 = str(self.gridx1) + "," + str(self.gridx2) + "," + str(self.gridy1 + 60) + "," + str(
            self.gridy2 + 60)
        keyname_9 = str(self.gridx1 + 100) + "," + str(self.gridx2 + 100) + "," + str(self.gridy1 + 60) + "," + str(
            self.gridy2 + 60)

        all_keys = [keyname_1, keyname_2, keyname_3, keyname_4, keyname_5, keyname_6, keyname_7, keyname_8, keyname_9]

        # checks if the key exist in the grid_subspaces, if the exist, append to meteorites_list the meteor objects
        for i in all_keys:
            if i in grid_subspaces:
                for meteor in grid_subspaces[i]:
                    if type(meteor) != Bullets and type(meteor) != Player:
                        meteorites_list.append(meteor)
        return meteorites_list

    def draw(self, win):
        win.blit(self.image, (self.xpos, self.ypos))


class Meteorites(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, mass, velocity, angle, img_file):
        pygame.sprite.Sprite.__init__(self)
        self.xpos = xpos
        self.ypos = ypos
        self.mass = mass
        self.velocity = velocity
        self.angle = angle
        self.image = img_file.convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        self.image_convert = self.image.convert()
        self.rotated_image = pygame.transform.rotate(self.image_convert, self.angle)
        self.change_x = 0
        self.change_y = 0
        self.rect_hit_box = ()
        self.id = uuid.uuid1()
        self.current_key = ""
        self.gridx1 = 0
        self.gridx2 = 0
        self.gridy1 = 0
        self.gridy2 = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.mask = pygame.mask.from_surface(self.image)
        # self.rect_object = pygame.Rect(self.xpos, self.ypos, self.width, self.height)

    def create_hit_box(self):
        self.rect_hit_box = (self.xpos, self.ypos, self.width, self.height)
        return self.rect_hit_box

    def get_rect(self):
        return pygame.Rect(self.xpos, self.ypos, self.width, self.height)

    def update_grid(self):
        prev_key_name = self.current_key

        # input into grid based on center of image, not the xpos/ypos
        img_width = self.image.get_width()
        img_height = self.image.get_height()
        x_grid_1 = round(((self.xpos + round(img_width // 2)) // 100) * 100)
        y_grid_1 = round(((self.ypos + round(img_height // 2)) // 60) * 60)

        x_grid_2 = x_grid_1 + 100
        y_grid_2 = y_grid_1 + 60
        key_name = str(x_grid_1) + "," + str(x_grid_2) + "," + str(y_grid_1) + "," + str(y_grid_2)

        self.gridx1 = x_grid_1
        self.gridx2 = x_grid_2
        self.gridy1 = y_grid_1
        self.gridy2 = y_grid_2

        self.current_key = key_name
        new_key_name = self.current_key
        if prev_key_name != new_key_name:
            if prev_key_name in grid_subspaces:
                grid_subspaces[prev_key_name].pop(self)

            if new_key_name in grid_subspaces:
                grid_subspaces[new_key_name][self] = 1

        return key_name

    def movement(self):
        if self.velocity != 0:
            self.change_x = math.sin(self.angle*math.pi/180)*self.velocity
            self.change_y = math.cos(self.angle*math.pi/180)*self.velocity
            self.xpos += self.change_x
            self.ypos += self.change_y

    def draw(self, win):
        win.blit(self.image, (self.xpos, self.ypos))
        # pygame.draw.rect(win, (255, 0, 0), self.create_hit_box(), 2)

    def get_mask(self):
        return pygame.mask.from_surface(self.rotated_image)

    def collision(self, meteorite):
        offset = (self.get_rect()[0] - meteorite.get_rect()[0], self.get_rect()[1] - meteorite.get_rect()[1])

        overlap = self.mask.overlap(meteorite.mask, offset)
        if overlap:
            print("hit")
            return True

        return False

    def hit(self):
        # get a list of meteorites in the surrounding grids a total of 9 grids 3x3 with center being the self meteor
        meteorites_list = []

        # keys of the surrounding grids 9 in total, 3x3
        keyname_1 = str(self.gridx1 - 100) + "," + str(self.gridx2 - 100) + "," + str(self.gridy1 - 60) + "," + str(self.gridy2 - 60)
        keyname_2 = str(self.gridx1) + "," + str(self.gridx2) + "," + str(self.gridy1 - 60) + "," + str(self.gridy2 - 60)
        keyname_3 = str(self.gridx1 + 100) + "," + str(self.gridx2 + 100) + "," + str(self.gridy1 - 60) + "," + str(self.gridy2 - 60)
        keyname_4 = str(self.gridx1 - 100) + "," + str(self.gridx2 - 100) + "," + str(self.gridy1) + "," + str(self.gridy2)
        keyname_5 = self.current_key
        keyname_6 = str(self.gridx1 + 100) + "," + str(self.gridx2 + 100) + "," + str(self.gridy1) + "," + str(self.gridy2)
        keyname_7 = str(self.gridx1 - 100) + "," + str(self.gridx2 - 100) + "," + str(self.gridy1 + 60) + "," + str(self.gridy2 + 60)
        keyname_8 = str(self.gridx1) + "," + str(self.gridx2) + "," + str(self.gridy1 + 60) + "," + str(self.gridy2 + 60)
        keyname_9 = str(self.gridx1 + 100) + "," + str(self.gridx2 + 100) + "," + str(self.gridy1 + 60) + "," + str(self.gridy2 + 60)

        all_keys = [keyname_1, keyname_2, keyname_3, keyname_4, keyname_5, keyname_6, keyname_7, keyname_8, keyname_9]

        # checks if the key exist in the grid_subspaces, if the exist, append to meteorites_list the meteor objects
        for i in all_keys:
            if i in grid_subspaces:
                for meteor in grid_subspaces[i]:
                    meteorites_list.append(meteor)
        for i in range(len(meteorites_list)):
            # make sure it is not the own meteorite
            if type(meteorites_list[i]) != Player:
                if meteorites_list[i].id != self.id:
                    # check if the xpos of meteorite overlaps with current meteorite
                    # if self.get_rect().colliderect(meteorites_list[i].get_rect()):
                    if self.collision(meteorites_list[i]):
                        # # apply the elastic collision momentum formula to get a new x and y velocities
                        sum_of_mass = meteorites_list[i].mass + self.mass
                        diff_of_mass = meteorites_list[i].mass - self.mass
                        x_vel_i_final = (diff_of_mass/sum_of_mass) * meteorites_list[i].change_x + ((self.mass * 2)/sum_of_mass) * self.change_x
                        x_vel_self_final = (-1*diff_of_mass/sum_of_mass) * self.change_x + ((meteorites_list[i].mass * 2)/sum_of_mass) * meteorites_list[i].change_x
                        y_vel_i_final = (diff_of_mass/sum_of_mass) * meteorites_list[i].change_y + ((self.mass * 2)/sum_of_mass) * self.change_y
                        y_vel_self_final = (-1*diff_of_mass/sum_of_mass) * self.change_y + ((meteorites_list[i].mass * 2)/sum_of_mass) * meteorites_list[i].change_y

                        # use the new x and y velocities to get the new angle and new non-vectorised velocity
                        meteorites_list[i].velocity = (x_vel_i_final ** 2 + y_vel_i_final ** 2) ** 0.5
                        self.velocity = (x_vel_self_final ** 2 + y_vel_self_final ** 2) ** 0.5

                        if meteorites_list[i].velocity != 0:
                            meteorites_list[i].angle = math.acos(y_vel_i_final/meteorites_list[i].velocity) * (180 / math.pi)

                        if self.velocity != 0:
                            self.angle = math.acos(y_vel_self_final/self.velocity) * (180 / math.pi)


def draw_canvas(player, meteorites_list, bullet_list, win):
    win.fill(BLACK)

    for meteor in meteorites_list:
        meteor.update_grid()
        meteor.create_hit_box()
        meteor.draw(win)
        # meteor.hit()
        meteor.movement()

    for bullet in bullet_list:
        bullet.update_grid()
        bullet.draw(win)
        # win.blit(bullet.image, (bullet.xpos, bullet.ypos))
        bullet.movement()

    player.update_grid()
    player.draw(win)
    pygame.display.flip()


def generate_meteors(state, meteorites_list):
    if state == "Test":
        number_of_starting_meteorites = 3
        x_pos = [screen_width - 100, 50, screen_width / 2]
        y_pos = [screen_height / 2, screen_height / 2, 50]
        angle_list = [270, 90, 360]
        for i in range(number_of_starting_meteorites):
            xpos_generator = x_pos[i]
            ypos_generator = y_pos[i]
            size_generator = random.randint(1, 4)
            meteor_chosen = random.choice(types_meteor_dict[size_generator][1])
            meteor_angle = angle_list[i]
            meteor_velocity = random.randint(types_meteor_dict[size_generator][0][1][0],
                                             types_meteor_dict[size_generator][0][1][1])
            meteor_mass = types_meteor_dict[size_generator][0][0]
            meteor_created = Meteorites(xpos_generator, ypos_generator, meteor_mass, meteor_velocity, meteor_angle,
                                        meteor_chosen)
            meteorites_list.append(meteor_created)

    if state == "Start":
        number_of_starting_meteorites = random.randint(10, 20)
        for i in range(number_of_starting_meteorites):
            xpos_generator = random.randint(10, screen_width - 100)
            ypos_generator = random.randint(10, screen_height - 50)
            size_generator = random.randint(1, 4)
            meteor_chosen = random.choice(types_meteor_dict[size_generator][1])
            meteor_angle = random.randint(1, 360)
            meteor_velocity = random.randint(types_meteor_dict[size_generator][0][1][0],
                                             types_meteor_dict[size_generator][0][1][1])
            meteor_mass = types_meteor_dict[size_generator][0][0]
            meteor_created = Meteorites(xpos_generator, ypos_generator, meteor_mass, meteor_velocity, meteor_angle,
                                        meteor_chosen)
            meteorites_list.append(meteor_created)

    elif state == "Left":
        number_of_starting_meteorites = random.randint(1, 2)
        for i in range(number_of_starting_meteorites):
            xpos_generator = random.randint(-50, -25)
            ypos_generator = random.randint(10, screen_height - 50)
            size_generator = random.randint(1, 4)
            meteor_chosen = random.choice(types_meteor_dict[size_generator][1])
            meteor_angle = random.randint(45, 135)
            meteor_velocity = random.randint(types_meteor_dict[size_generator][0][1][0],
                                             types_meteor_dict[size_generator][0][1][1])
            meteor_mass = types_meteor_dict[size_generator][0][0]
            meteor_created = Meteorites(xpos_generator, ypos_generator, meteor_mass, meteor_velocity, meteor_angle,
                                        meteor_chosen)
            meteorites_list.append(meteor_created)

    elif state == "Right":
        number_of_starting_meteorites = random.randint(1, 2)
        for i in range(number_of_starting_meteorites):
            xpos_generator = random.randint(screen_width + 25, screen_width + 50)
            ypos_generator = random.randint(10, screen_height - 50)
            size_generator = random.randint(1, 4)
            meteor_chosen = random.choice(types_meteor_dict[size_generator][1])
            meteor_angle = random.randint(225, 315)
            meteor_velocity = random.randint(types_meteor_dict[size_generator][0][1][0],
                                             types_meteor_dict[size_generator][0][1][1])
            meteor_mass = types_meteor_dict[size_generator][0][0]
            meteor_created = Meteorites(xpos_generator, ypos_generator, meteor_mass, meteor_velocity, meteor_angle,
                                        meteor_chosen)
            meteorites_list.append(meteor_created)

    elif state == "Up":
        number_of_starting_meteorites = random.randint(1, 2)
        for i in range(number_of_starting_meteorites):
            xpos_generator = random.randint(10, screen_width - 100)
            ypos_generator = random.randint(-50, -25)
            size_generator = random.randint(1, 4)
            meteor_chosen = random.choice(types_meteor_dict[size_generator][1])
            meteor_angle = random.randint(315, 405)
            meteor_velocity = random.randint(types_meteor_dict[size_generator][0][1][0],
                                             types_meteor_dict[size_generator][0][1][1])
            meteor_mass = types_meteor_dict[size_generator][0][0]
            meteor_created = Meteorites(xpos_generator, ypos_generator, meteor_mass, meteor_velocity, meteor_angle,
                                        meteor_chosen)
            meteorites_list.append(meteor_created)

    elif state == "Down":
        number_of_starting_meteorites = random.randint(1, 2)
        for i in range(number_of_starting_meteorites):
            xpos_generator = random.randint(10, screen_width - 100)
            ypos_generator = random.randint(screen_height + 25, screen_height + 50)
            size_generator = random.randint(1, 4)
            meteor_chosen = random.choice(types_meteor_dict[size_generator][1])
            meteor_angle = random.randint(135, 225)
            meteor_velocity = random.randint(types_meteor_dict[size_generator][0][1][0],
                                             types_meteor_dict[size_generator][0][1][1])
            meteor_mass = types_meteor_dict[size_generator][0][0]
            meteor_created = Meteorites(xpos_generator, ypos_generator, meteor_mass, meteor_velocity, meteor_angle,
                                        meteor_chosen)
            meteorites_list.append(meteor_created)


def meteor_population_control(meteorites_list):
    fix_num_meteorites = 50
    if len(meteorites_list) > fix_num_meteorites:
        diff = len(meteorites_list) - fix_num_meteorites
        meteorites_list = meteorites_list[diff:]

    return meteorites_list
    # print(len(meteorites_list))


def main():
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60

    win = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Asteroids")
    running = True

    # generating player
    player = Player(player_file_name)
    player.angle = 0
    player_image_copy = pygame.transform.rotate(player.image_convert, player.angle)
    starting_pos = (screen_width/2 - 20 - player.xpos, screen_height/2 - 20 - player.ypos)
    player.xpos = starting_pos[0] + int(player_image_copy.get_width() / 2)
    player.ypos = starting_pos[1] + int(player_image_copy.get_height() / 2)
    win.blit(player.image, tuple(starting_pos))

    # generating starting meteorites
    # to store all the created starting meteorites
    meteorites_list = []
    generate_meteors("Start", meteorites_list)

    # store bullets into a list
    bullet_list = []

    freq_mg = 0
    freq_mr = 0
    shootloop = 0
    while running:
        clock.tick(fps)

        if shootloop > 0:
            shootloop += 1

        if shootloop > 20:
            shootloop = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.movement()

        if keys[pygame.K_a]:
            player.angle += 6
            
        if keys[pygame.K_s]:
            player.angle -= 6

        if keys[pygame.K_d] and shootloop == 0:
            new_bullet = Bullets(0, 0, 0)
            new_bullet.xpos = player.xpos - new_bullet.width*(1 - math.sin(player.angle*math.pi/180)) / 2
            new_bullet.ypos = player.ypos - new_bullet.width*(1 - math.cos(player.angle*math.pi/180)) / 2
            new_bullet.angle = player.angle
            bullet_list.append(new_bullet)
            shootloop = 1

        side = ["Up", "Down", "Left", "Right"]
        if freq_mg == 10:
            # generate_meteors("Test", meteorites_list)
            generate_meteors(random.choice(side), meteorites_list)
            freq_mg = 0

        # to control meteorites list size
        if freq_mr == 100:
            meteorites_list = meteor_population_control(meteorites_list)
            freq_mr = 0

        freq_mg += 1
        freq_mr += 1

        close_meteors = player.check_proximity()
        player_mask = pygame.mask.from_surface(pygame.transform.rotate(player.image_convert, player.angle))
        for meteor in close_meteors:
            offset = (player.get_rect()[0] - meteor.get_rect()[0], player.get_rect()[1] - meteor.get_rect()[1])
            # overlap = player_mask.overlap(meteor.mask, offset)
            overlap = player.get_rect().colliderect(meteor.get_rect())
            if overlap:
                if meteor in grid_subspaces[player.current_key].keys():
                    grid_subspaces[player.current_key].pop(meteor)
                    meteorites_list.pop(meteorites_list.index(meteor))

        for bullet in bullet_list:
            b_close_meteor = bullet.check_proximity()
            for meteor in b_close_meteor:
                # offset = (bullet.get_rect()[0] - meteor.get_rect()[0], bullet.get_rect()[1] - meteor.get_rect()[1])
                # overlap = player_mask.overlap(meteor.mask, offset)
                overlap = bullet.get_rect().colliderect(meteor.get_rect())
                if overlap:
                    if bullet.current_key in grid_subspaces.keys():
                        if meteor in grid_subspaces[bullet.current_key].keys():
                            grid_subspaces[bullet.current_key].pop(meteor)
                            meteorites_list.pop(meteorites_list.index(meteor))

                            # remove bullet
                            grid_subspaces[bullet.current_key].pop(bullet)
                            bullet_list.pop(bullet_list.index(bullet))


        draw_canvas(player, meteorites_list, bullet_list, win)


if __name__ == "__main__":
    main()
