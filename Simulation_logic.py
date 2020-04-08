from random import uniform, randrange
from math import sqrt

class Sheep:
    max_x = 1000
    max_y = 1000

    def __init__(self, nr, init_pos_limit, sheep_move_dist):
        self.__nr = nr
        self.__is_live = True
        self.__pos_x = uniform(-init_pos_limit, init_pos_limit)  # Randomowy float z przedzialu
        self.__pos_y = uniform(-init_pos_limit, init_pos_limit)
        self.__move_dist = sheep_move_dist  # Pilnowac zeby bylo dodatnie

    # Getters
    def get_pos_x(self):
        return self.__pos_x

    def get_pos_y(self):
        return self.__pos_y

    def get_nr(self):
        return self.__nr

    def get_is_live(self):
        return self.__is_live

    def get_distance(self):
        return self.__move_dist

    # Setters
    def set_pos_x(self, dist):
        self.__pos_x = dist

    def set_pos_y(self, dist):
        self.__pos_y = dist

    def set_nr(self, nr):
        self.__nr = nr

    def update_pos_x(self, dist):
        if self.__pos_x + dist > self.max_x:
            self.__pos_x = self.max_x
        elif self.__pos_x + dist < 0:
            self.__pos_x = 0
        else:
            self.__pos_x += dist

    def update_pos_y(self, dist):
        if self.__pos_y + dist > self.max_y:
            self.__pos_y = self.max_y
        elif self.__pos_y + dist < 0:
            self.__pos_y = 0
        else:
            self.__pos_y += dist

    def set_live_flag_to_death(self):
        self.__is_live = False

    def test(self, x, y):
        self.__pos_x = x
        self.__pos_y = y

    # 1 po osi x w strone dodatnich
    # 2 po osi x w strone ujemnych
    # 3 po osi y w gore
    # 4 po osi y w dol
    def move_sheep(self):
        tmp = randrange(1, 4)
        if tmp == 1:
            self.update_pos_x(self.__move_dist)
        elif tmp == 2:
            self.update_pos_x(self.__move_dist*(-1))
        elif tmp == 3:
            self.update_pos_y(self.__move_dist)
        else:
            self.update_pos_y(self.__move_dist*(-1))


class Wolf:
    max_x = 1000
    max_y = 1000

    def __init__(self, wolf_move_dist):
        self.__pos_x = (1.5 * 500) / 2          # srodek z init_pos_limit z Interface
        self.__pos_y = (1.5 * 500) / 2
        self.__move_dist = wolf_move_dist

    # Getters
    def get_pos_x(self):
        return self.__pos_x

    def get_pos_y(self):
        return self.__pos_y

    def get_distance(self):
        return self.__move_dist

    # Setters
    def set_pos_x(self, dist):
        self.__pos_x = dist

    def set_pos_y(self, dist):
        self.__pos_y = dist

    def set_pos_after_attack(self, x, y):
        self.__pos_x = x
        self.__pos_y = y

    # Pitagoras xd
    def calculate_distance_to_sheep(self, sheep):
        x = sheep.get_pos_x() - self.__pos_x
        y = sheep.get_pos_y() - self.__pos_y
        result = x**2 + y**2
        return sqrt(result)

    # Jak atakuje to idzie na jej miejsce
    def attack(self, sheep):
        self.set_pos_after_attack(sheep.get_pos_x(), sheep.get_pos_y())
        sheep.set_live_flag_to_death()

    def chase_target(self, sheep):
        distance = sqrt((self.__pos_x - sheep.get_pos_x())**2 + (self.__pos_y - sheep.get_pos_y())**2)

        if sheep.get_pos_y() > self.get_pos_y():
            new_y = (self.get_distance() * sheep.get_pos_y() - self.get_distance() * self.get_pos_y()
                     + self.get_pos_y() * distance) / distance
            if new_y > self.max_y:
                self.__pos_y = self.max_y
            elif new_y < 0:
                self.__pos_y = 0
            else:
                self.__pos_y = new_y

        else:
            new_y = (self.get_pos_y() * distance - self.get_distance() * self.get_pos_y()
                     + self.get_distance() * sheep.get_pos_y()) / distance
            if new_y > self.max_y:
                self.__pos_y = self.max_y
            elif new_y < 0:
                self.__pos_y = 0
            else:
                self.__pos_y = new_y

        if sheep.get_pos_x() > self.get_pos_x():
            new_x = (self.get_distance() * sheep.get_pos_x() - self.get_distance() * self.get_pos_x()
                     + self.get_pos_x() * distance) / distance
            if new_x > self.max_x:
                self.__pos_x = self.max_x
            elif new_x < 0:
                self.__pos_x = 0
            else:
                self.__pos_x = new_x
        else:
            new_x = (self.get_pos_x() * distance - self.get_distance() * self.get_pos_x()
                     + self.get_distance() * sheep.get_pos_x()) / distance
            if new_x > self.max_x:
                self.__pos_x = self.max_x
            elif new_x < 0:
                self.__pos_x = 0
            else:
                self.__pos_x = new_x

    def choose_sheep(self, sheep_list):
        tmp = self.calculate_distance_to_sheep(sheep_list[0])
        nearest_sheep = sheep_list[0]
        for sheep in sheep_list:
            if self.calculate_distance_to_sheep(sheep) < tmp:
                tmp = self.calculate_distance_to_sheep(sheep)
                nearest_sheep = sheep
        return nearest_sheep

