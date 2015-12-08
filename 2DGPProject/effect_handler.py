

class EffectHandler(object):
    
    def __init__(self):
        self.effects = []


    def update(self, frame_time):
        for effect in self.effects:
            effect.update(frame_time)
            if effect.destroyed:
                self.effects.remove(effect)


    def draw(self):
        for effect in effects:
            effect.draw()


    def add_effect(self, effect):
        self.effects.append(effect)
