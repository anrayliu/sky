import math 


def move_by_angle(pos, angle, distance, degrees=False):
    if degrees:
        angle = math.radians(angle)
    return (pos[0] + math.cos(angle) * distance, pos[1] + math.sin(angle) * distance)
    
def add_tuple(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])
    
