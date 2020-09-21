#a track is a list of tuples of coordinates which create a loop


class Track:
    track1 = [[(60,36), (60, 684)],
         [(60,36), (1220, 36)],
         [(60, 684), (1220, 684)],
         [(1220, 684), (1220, 36)],
         [(180, 156), (180, 576)],
         [(180, 576), (1100, 576)],
         [(1100, 156), (1100, 576)],
         [(180, 156), (1100, 156)]]

    start_finish1 = [(60, 384), (180, 384)]
    line_thickness = 5
    #TODO somehow incorperate start finish into list of tracks

    def __init__(track_coords = track1, start_finish = start_finish1):
        track_coords = track_coords
        start_finish = start_finish
        


        