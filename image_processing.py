from copy import deepcopy
from itertools import combinations
from pprint import pformat
from subprocess import check_output
import argparse
import cv2
import logging
import json
import logging
import math
import numpy as np
import os
import sys
import time
import subprocess

log = logging.getLogger(__name__)

def pixel_distance(A, B):
    """
    Return the distance between two pixels
    """
    (col_A, row_A) = A
    (col_B, row_B) = B

    return math.sqrt(math.pow(col_B - col_A, 2) + math.pow(row_B - row_A, 2))


def get_angle(A, B, C):
    """
    Return the angle at C (in radians) for the triangle formed by A, B, C
    """
    (col_A, row_A) = A
    (col_B, row_B) = B
    (col_C, row_C) = C
    a = pixel_distance(C, B)
    b = pixel_distance(A, C)
    c = pixel_distance(A, B)

    try:
        cos_angle = (math.pow(a, 2) + math.pow(b, 2) - math.pow(c, 2)) / (2 * a * b)
    except ZeroDivisionError as e:
        log.warning("get_angle: A %s, B %s, C %s, a %.3f, b %.3f, c %.3f" % (A, B, C, a, b, c))
        raise e

    # If CA and CB are very long and the angle at C very narrow we can get an
    # invalid cos_angle which will cause math.acos() to raise a ValueError exception
    if cos_angle > 1:
        cos_angle = 1
    elif cos_angle < -1:
        cos_angle = -1

    angle_ACB = math.acos(cos_angle)
    return angle_ACB


def sort_corners(corner1, corner2, corner3, corner4):
    """
    Sort the corners such that
    - A is top left
    - B is top right
    - C is bottom left
    - D is bottom right

    Return an (A, B, C, D) tuple
    """
    results = []
    corners = (corner1, corner2, corner3, corner4)

    min_x = None
    max_x = None
    min_y = None
    max_y = None

    for (x, y) in corners:
        if min_x is None or x < min_x:
            min_x = x

        if max_x is None or x > max_x:
            max_x = x

        if min_y is None or y < min_y:
            min_y = y

        if max_y is None or y > max_y:
            max_y = y

    # top left
    top_left = None
    top_left_distance = None
    for (x, y) in corners:
        distance = pixel_distance((min_x, min_y), (x, y))
        if top_left_distance is None or distance < top_left_distance:
            top_left = (x, y)
            top_left_distance = distance

    results.append(top_left)

    # top right
    top_right = None
    top_right_distance = None

    for (x, y) in corners:
        if (x, y) in results:
            continue

        distance = pixel_distance((max_x, min_y), (x, y))
        if top_right_distance is None or distance < top_right_distance:
            top_right = (x, y)
            top_right_distance = distance
    results.append(top_right)

    # bottom left
    bottom_left = None
    bottom_left_distance = None

    for (x, y) in corners:
        if (x, y) in results:
            continue

        distance = pixel_distance((min_x, max_y), (x, y))

        if bottom_left_distance is None or distance < bottom_left_distance:
            bottom_left = (x, y)
            bottom_left_distance = distance
    results.append(bottom_left)

    # bottom right
    bottom_right = None
    bottom_right_distance = None

    for (x, y) in corners:
        if (x, y) in results:
            continue

        distance = pixel_distance((max_x, max_y), (x, y))

        if bottom_right_distance is None or distance < bottom_right_distance:
            bottom_right = (x, y)
            bottom_right_distance = distance
    results.append(bottom_right)

    return results


def approx_is_square(approx, SIDE_VS_SIDE_THRESHOLD=0.60, ANGLE_THRESHOLD=20, ROTATE_THRESHOLD=30):
    """
    Rules
    - there must be four corners
    - all four lines must be roughly the same length
    - all four corners must be roughly 90 degrees
    - AB and CD must be horizontal lines
    - AC and BC must be vertical lines

    SIDE_VS_SIDE_THRESHOLD
        If this is 1 then all 4 sides must be the exact same length.  If it is
        less than one that all sides must be within the percentage length of
        the longest side.

    ANGLE_THRESHOLD
        If this is 0 then all 4 corners must be exactly 90 degrees.  If it
        is 10 then all four corners must be between 80 and 100 degrees.

    ROTATE_THRESHOLD
        Controls how many degrees the entire square can be rotated

    The corners are labeled

        A ---- B
        |      |
        |      |
        C ---- D
    """

    assert SIDE_VS_SIDE_THRESHOLD >= 0 and SIDE_VS_SIDE_THRESHOLD <= 1, "SIDE_VS_SIDE_THRESHOLD must be between 0 and 1"
    assert ANGLE_THRESHOLD >= 0 and ANGLE_THRESHOLD <= 90, "ANGLE_THRESHOLD must be between 0 and 90"

    # There must be four corners
    if len(approx) != 4:
        return False

    # Find the four corners
    (A, B, C, D) = sort_corners(tuple(approx[0][0]),
                                tuple(approx[1][0]),
                                tuple(approx[2][0]),
                                tuple(approx[3][0]))

    # Find the lengths of all four sides
    AB = pixel_distance(A, B)
    AC = pixel_distance(A, C)
    DB = pixel_distance(D, B)
    DC = pixel_distance(D, C)
    distances = (AB, AC, DB, DC)
    max_distance = max(distances)
    cutoff = int(max_distance * SIDE_VS_SIDE_THRESHOLD)


    # If any side is much smaller than the longest side, return False
    for distance in distances:
        if distance < cutoff:
            return False

    # all four corners must be roughly 90 degrees
    min_angle = 90 - ANGLE_THRESHOLD
    max_angle = 90 + ANGLE_THRESHOLD

    # Angle at A
    angle_A = int(math.degrees(get_angle(C, B, A)))
    if angle_A < min_angle or angle_A > max_angle:
        return False

    # Angle at B
    angle_B = int(math.degrees(get_angle(A, D, B)))
    if angle_B < min_angle or angle_B > max_angle:
        return False

    # Angle at C
    angle_C = int(math.degrees(get_angle(A, D, C)))
    if angle_C < min_angle or angle_C > max_angle:
        return False

    # Angle at D
    angle_D = int(math.degrees(get_angle(C, B, D)))
    if angle_D < min_angle or angle_D > max_angle:
        return False

    far_left  = min(A[0], B[0], C[0], D[0])
    far_right = max(A[0], B[0], C[0], D[0])
    far_up    = min(A[1], B[1], C[1], D[1])
    far_down  = max(A[1], B[1], C[1], D[1])
    top_left = (far_left, far_up)
    top_right = (far_right, far_up)
    bottom_left = (far_left, far_down)
    bottom_right = (far_right, far_down)
    debug = False


    # Is AB horizontal?
    if B[1] < A[1]:
        # Angle at B relative to the AB line
        angle_B = int(math.degrees(get_angle(A, top_left, B)))

        if debug:
            log.info("AB is horizontal, angle_B %s, ROTATE_THRESHOLD %s" % (angle_B, ROTATE_THRESHOLD))

        if angle_B > ROTATE_THRESHOLD:
            if debug:
                log.info("AB horizontal rotation %s is above ROTATE_THRESHOLD %s" % (angle_B, ROTATE_THRESHOLD))
            return False
    else:
        # Angle at A relative to the AB line
        angle_A = int(math.degrees(get_angle(B, top_right, A)))

        if debug:
            log.info("AB is vertical, angle_A %s, ROTATE_THRESHOLD %s" % (angle_A, ROTATE_THRESHOLD))

        if angle_A > ROTATE_THRESHOLD:
            if debug:
                log.info("AB vertical rotation %s is above ROTATE_THRESHOLD %s" % (angle_A, ROTATE_THRESHOLD))
            return False

    return True

def square_width_height(approx, debug):
    """
    This assumes that approx is a square. Return the width and height of the square.
    """
    width = 0
    height = 0

    # Find the four corners
    (A, B, C, D) = sort_corners(tuple(approx[0][0]),
                                tuple(approx[1][0]),
                                tuple(approx[2][0]),
                                tuple(approx[3][0]))

    # Find the lengths of all four sides
    AB = pixel_distance(A, B)
    AC = pixel_distance(A, C)
    DB = pixel_distance(D, B)
    DC = pixel_distance(D, C)

    width = max(AB, DC)
    height = max(AC, DB)

    if debug:
        log.info("square_width_height: AB %d, AC %d, DB %d, DC %d, width %d, height %d" % (AB, AC, DB, DC, width, height))

    return (width, height)

def compress_2d_array(original):
    """
    Convert 2d array to a 1d array
    """
    result = []
    for row in original:
        for col in row:
            result.append(col)
    return result


class CustomContour(object):

    def __init__(self, rubiks_parent, index, contour, heirarchy, debug):
        self.rubiks_parent = rubiks_parent
        self.index = index
        self.contour = contour
        self.heirarchy = heirarchy
        peri = cv2.arcLength(contour, True)
        self.approx = cv2.approxPolyDP(contour, 0.1 * peri, True)
        self.area = cv2.contourArea(contour)
        self.corners = len(self.approx)
        self.width = None
        self.debug = debug

        # compute the center of the contour
        M = cv2.moments(contour)

        if M["m00"]:
            self.cX = int(M["m10"] / M["m00"])
            self.cY = int(M["m01"] / M["m00"])

        else:
            self.cX = None
            self.cY = None

    def __str__(self):
        return "Contour #%d (%s, %s)" % (self.index, self.cX, self.cY)

    def is_square(self, target_area=None):

        if self.rubiks_parent.size == 6:
            AREA_THRESHOLD = 0.50
        else:
            AREA_THRESHOLD = 0.25

        if not approx_is_square(self.approx):
            return False

        if self.width is None:
            (self.width, self.height) = square_width_height(self.approx, self.debug)

        if target_area:
            area_ratio = float(target_area / self.area)

            if area_ratio < float(1.0 - AREA_THRESHOLD) or area_ratio > float(1.0 + AREA_THRESHOLD):
                return False
            else:
                return True
        else:
            return True

    def get_child(self):
        # Each contour has its own information regarding what hierarchy it
        # is, who is its parent, who is its parent etc. OpenCV represents it as
        # an array of four values : [Next, Previous, First_parent, Parent]
        child = self.heirarchy[2]

        if child != -1:
            return self.rubiks_parent.contours_by_index[child]
        return None

    def child_is_square(self):
        """
        The black border between the squares can cause us to sometimes find a
        contour for the outside edge of the border and a contour for the the
        inside edge.  This function returns True if this contour is the outside
        contour in that scenario.
        """
        child_con = self.get_child()

        if child_con:
            # If there is a dent in a square sometimes you will get a really small
            # contour inside the square...we want to ignore those so make sure the
            # area of the inner square is close to the area of the outer square.
            if int(child_con.area * 3) < self.area:
                return False

            if child_con.is_square():
                return True

        return False

    def get_parent(self):
        # Each contour has its own information regarding what hierarchy it
        # is, who is its parent, who is its parent etc. OpenCV represents it as
        # an array of four values : [Next, Previous, First_parent, Parent]
        parent = self.heirarchy[3]

        if parent != -1:
            return self.rubiks_parent.contours_by_index[parent]
        return None

    def parent_is_candidate(self):
        parent_con = self.get_parent()

        if parent_con:
            if parent_con in self.rubiks_parent.candidates:
                return True

        return False

    def parent_is_square(self):
        parent_con = self.get_parent()

        if parent_con:
            # If there is a dent in a square sometimes you will get a really small
            # contour inside the square...we want to ignore those so make sure the
            # area of the inner square is close to the area of the outer square.
            if int(parent_con.area * 2) < self.area:
                return False

            if parent_con.is_square():
                return True

        return False

class RubiksOpenCV(object):

    def __init__(self,frame, index=0, name=None, debug=False):
        self.index = index
        self.name = name
        self.debug = debug
        self.image = None
        self.size_static = None
        self.reset()

    def __str__(self):
        return str(self.name)

    def reset(self):
        self.data = {}
        self.candidates = []
        self.contours_by_index = {}
        self.median_square_area = None
        self.black_border_width = None
        self.top                = None
        self.right              = None
        self.bottom             = None
        self.left               = None

        #3x3x3
        self.size = None

    def get_contour_neighbors(self, contours, target_con):
        """
        Return stats on how many other contours are in the same 'row' or 'col' as target_con
		"""
        row_neighbors = 0
        row_square_neighbors = 0
        col_neighbors = 0
        col_square_neighbors = 0

        # Wiggle +/- 50% the median_square_width
        if self.size is None:
            WIGGLE_THRESHOLD = 0.50

        elif self.size == 7:
            WIGGLE_THRESHOLD = 0.50

        else:
            WIGGLE_THRESHOLD = 0.70

        # width_wiggle determines how far left/right we look for other contours
        # height_wiggle determines how far up/down we look for other contours
        width_wiggle = int(self.median_square_width * WIGGLE_THRESHOLD)
        height_wiggle = int(self.median_square_width * WIGGLE_THRESHOLD)

        log.debug("get_contour_neighbors() for %s, median square width %s, width_wiggle %s, height_wiggle %s" %
            (target_con, self.median_square_width, width_wiggle, height_wiggle))

        for con in contours:

            # do not count yourself
            if con == target_con:
                continue

            x_delta = abs(con.cX - target_con.cX)
            y_delta = abs(con.cY - target_con.cY)

            if x_delta <= width_wiggle:
                col_neighbors += 1

                if con.is_square(self.median_square_area):
                    col_square_neighbors += 1
                    log.debug("%s is a square col neighbor" % con)
                else:
                    log.debug("%s is a non-square col neighbor, it has %d corners" % (con, con.corners))
            else:
                log.debug("%s x delta %s is outside width wiggle room %s" % (con, x_delta, width_wiggle))

            if y_delta <= height_wiggle:
                row_neighbors += 1

                if con.is_square(self.median_square_area):
                    row_square_neighbors += 1
                    log.debug("%s is a square row neighbor" % con)
                else:
                    log.debug("%s is a non-square row neighbor, it has %d corners" % (con, con.corners))
            else:
                log.debug("%s y delta %s is outside height wiggle room %s" % (con, y_delta, height_wiggle))

        
        return (row_neighbors, row_square_neighbors, col_neighbors, col_square_neighbors)

    def sort_by_row_col(self, contours, size):
        """
        Given a list of contours sort them starting from the upper left corner
        and ending at the bottom right corner
        """
        result = []
        num_squares = len(contours)

        for row_index in range(size):

            # We want the 'size' squares that are closest to the top
            tmp = []
            for con in contours:
                tmp.append((con.cY, con.cX))
            top_row = sorted(tmp)[:size]

            # Now that we have those, sort them from left to right
            top_row_left_right = []
            for (cY, cX) in top_row:
                top_row_left_right.append((cX, cY))
            top_row_left_right = sorted(top_row_left_right)

            log.debug("sort_by_row_col() row %d: %s" % (row_index, pformat(top_row_left_right)))
            contours_to_remove = []
            for (target_cX, target_cY) in top_row_left_right:
                for con in contours:

                    if con in contours_to_remove:
                        continue

                    if con.cX == target_cX and con.cY == target_cY:
                        result.append(con)
                        contours_to_remove.append(con)
                        break

            for con in contours_to_remove:
                contours.remove(con)

        #assert len(result) == num_squares, "Returning %d squares, it should be %d" % (len(result), num_squares)
        return result

    def remove_non_square_candidates(self, median_square_area=None):
        """
        Remove non-square contours from candidates.  Return a list of the ones we removed.
        """
        candidates_to_remove = []

        for con in self.candidates:
            if not con.is_square(median_square_area):
                candidates_to_remove.append(con)

        for x in candidates_to_remove:
            self.candidates.remove(x)

            #if self.debug:
            #    log.info("removing non-square contour %s" % x)

        removed = len(candidates_to_remove)

        if self.debug:
            log.info("remove-non-square-candidates: %d removed, %d remain, median_square_area %s" %
                (removed, len(self.candidates), median_square_area))

        if removed:
            return True
        else:
            return False

    def remove_dwarf_candidates(self, area_cutoff):
        candidates_to_remove = []

        # Remove parents with square child contours
        for con in self.candidates:
            if con.area < area_cutoff:
                candidates_to_remove.append(con)

        for x in candidates_to_remove:
            self.candidates.remove(x)

        removed = len(candidates_to_remove)
        log.debug("remove-dwarf-candidates %d removed, %d remain" % (removed, len(self.candidates)))
        return candidates_to_remove

    def remove_gigantic_candidates(self, area_cutoff):
        candidates_to_remove = []

        # Remove parents with square child contours
        for con in self.candidates:
            if con.area > area_cutoff:
                candidates_to_remove.append(con)
                if self.debug:
                    log.info("remove_gigantic_candidates: %s area %d is greater than cutoff %d" % (con, con.area, area_cutoff))

        for x in candidates_to_remove:
            self.candidates.remove(x)

        removed = len(candidates_to_remove)

        if self.debug:
            log.info("remove-gigantic-candidates: %d removed, %d remain" % (removed, len(self.candidates)))

        return candidates_to_remove

    def remove_square_within_square_candidates(self):
        candidates_to_remove = []

        # Remove parents with square child contours
        for con in self.candidates:
            if con.is_square() and con.child_is_square():
                candidates_to_remove.append(con)

        # Remove contours whose parents are square
        for con in self.candidates:
            if con in candidates_to_remove:
                continue

            # The parent must be a square but cannot be a gigantic square (ie
            # the entire edge of the picture had a contour). Gigantic squares
            # have been removed from the candidates by the time we get here.
            if con.parent_is_candidate() and con.parent_is_square():
                parent = con.get_parent()

                if parent not in candidates_to_remove:
                    candidates_to_remove.append(con)

        for x in candidates_to_remove:
            self.candidates.remove(x)

        removed = len(candidates_to_remove)
        log.debug("remove-square-within-square-candidates %d removed, %d remain" % (removed, len(self.candidates)))
        return True if removed else False

    def get_median_square_area(self):
        """
        Find the median area of all square contours
        """
        square_areas = []
        square_widths = []

        for con in self.candidates:
            if con.is_square():
                square_areas.append(int(con.area))
                square_widths.append(int(con.width))

        if square_areas:
            square_areas = sorted(square_areas)
            square_widths = sorted(square_widths)
            num_squares = len(square_areas)

            # Do not take the exact median, take the one 2/3 of the way through
            # the list. Sometimes you get clusters of smaller squares which can
            # throw us off if we take the exact median.
            square_area_index = int((2 * num_squares)/3)

            self.median_square_area = int(square_areas[square_area_index])
            self.median_square_width = int(square_widths[square_area_index])

            if self.debug:
                log.info("get_median_square_area: %d squares, median index %d, median area %d, all square areas %s" %\
                    (num_squares, square_area_index, self.median_square_area, ','.join(map(str, square_areas))))
                log.info("get_median_square_area: %d squares, median index %d, median width %d, all square widths %s" %\
                    (num_squares, square_area_index, self.median_square_width, ','.join(map(str, square_widths))))

        return True if square_areas else False

    def get_cube_boundry(self, strict):
        """
        Find the top, right, bottom, left boundry of all square contours
        """
        self.top    = None
        self.right  = None
        self.bottom = None
        self.left   = None

        for con in self.candidates:
            if con.is_square(self.median_square_area):
                (row_neighbors, row_square_neighbors, col_neighbors, col_square_neighbors) =\
                    self.get_contour_neighbors(self.candidates, con)

                if self.debug:
                    log.info("get_cube_boundry: %s contour is square, row_neighbors %s, col_neighbors %s" %
                        (con, row_square_neighbors, col_square_neighbors))

                # Ignore the rogue square with no neighbors. I used to do an "or" here but
                # that was too strict for 2x2x2 cubes.
                if not row_square_neighbors and not col_square_neighbors:
                    continue

                if self.top is None or con.cY < self.top:
                    self.top = con.cY

                if self.bottom is None or con.cY > self.bottom:
                    self.bottom = con.cY

                if self.left is None or con.cX < self.left:
                    self.left = con.cX

                if self.right is None or con.cX > self.right:
                    self.right = con.cX

        if self.size:
            if self.debug:
                log.info("get_cube_boundry: size %s, strict %s, top %s, bottom %s, left %s right %s" %
                    (self.size, strict, self.top, self.bottom, self.left, self.right))

        if self.top:
            return True
        else:
            return False

    def get_cube_size(self):
        """
        Look at all of the contours that are squares and see how many square
        neighbors they have in their row and col. Store the number of square
        contours in each row/col in data, then sort data and return the
        median entry
        """

        size_count = {}
        self.size = None

        for con in self.candidates:
            if con.is_square(self.median_square_area):
                (row_neighbors, row_square_neighbors, col_neighbors, col_square_neighbors) =\
                    self.get_contour_neighbors(self.candidates, con)
                row_size = row_neighbors + 1
                col_size = col_neighbors + 1
                log.debug("%s has %d row size, %d col size" % (con, row_size, col_size))

                if row_size not in size_count:
                    size_count[row_size] = 0
                size_count[row_size] += 1

                if col_size not in size_count:
                    size_count[col_size] = 0
                size_count[col_size] += 1

        # Find the size count entry with the highest value, that is our cube size
        cube_size = None
        cube_size_count = 0

        for size in sorted(size_count.keys()):
            count = size_count[size]

            if cube_size is None or count > cube_size_count or (count == cube_size_count and size > cube_size):
                cube_size = size
                cube_size_count = count

        if cube_size == 1:
            self.size = None
        else:

            # self.size_static is None by default and is only set when running in --webcam mode
            if self.size_static is None or cube_size == self.size_static:
                self.size = cube_size

        if self.debug:
            log.info("cube size is %s, size_count %s" % (self.size, pformat(size_count)))

        # Return True if we found a valid cube size
        return self.size == 3

    def set_contour_row_col_index(self, con):
        cube_height = self.bottom - self.top + self.median_square_width + self.black_border_width
        cube_width = self.right - self.left + self.median_square_width + self.black_border_width

        row_size = int(cube_height / (self.median_square_width + self.black_border_width))
        row_size = min(self.size, row_size)
        median_row_height = float(cube_height / row_size)

        col_size = int(cube_width / (self.median_square_width + self.black_border_width))
        col_size = min(self.size, col_size)
        median_col_width = float(cube_width / col_size)

        if self.debug:
            log.info("set_contour_row_col_index %s, top %d, bottom %d, cube_height %d, row_size %s, median_row_height %s, median_square_width %d" %
                (con, self.top, self.bottom, cube_height, row_size, median_row_height, self.median_square_width))
            log.info("set_contour_row_col_index %s, left %d, right %d, cube_width %d, col_size %s, median_col_width %s, median_square_width %d" %
                (con, self.left, self.right, cube_width, col_size, median_col_width, self.median_square_width))

        con.row_index = int(round((con.cY - self.top)/median_row_height))
        con.col_index = int(round((con.cX - self.left)/median_col_width))

        assert con.row_index < self.size, "con.row_index is %d, must be less than size %d" % (con.row_index, self.size)
        assert con.col_index < self.size, "con.col_index is %d, must be less than size %d" % (con.col_index, self.size)

        if self.debug:
            log.info("set_contour_row_col_index %s, col_index %d, row_index %d\n" % (con, con.col_index, con.row_index))

    def remove_contours_outside_cube(self, contours):
        assert self.median_square_area is not None, "get_median_square_area() must be called first"
        contours_to_remove = []

        # Give a little wiggle room
        top    = self.top    - int(self.median_square_width/4)
        bottom = self.bottom + int(self.median_square_width/4)
        left   = self.left   - int(self.median_square_width/4)
        right  = self.right  + int(self.median_square_width/4)

        for con in contours:
            if con.cY < top or con.cY > bottom or con.cX < left or con.cX > right:
                contours_to_remove.append(con)

        for con in contours_to_remove:
            contours.remove(con)

        removed = len(contours_to_remove)
        log.debug("remove-contours-outside-cube %d removed, %d remain" % (removed, len(contours)))
        return True if removed else False

    def get_black_border_width(self):
        cube_height = self.bottom - self.top
        cube_width = self.right - self.left

        if cube_width > cube_height:
            pixels = cube_width
            pixels_desc = 'width'
        else:
            pixels = cube_height
            pixels_desc = 'height'

        DILATION_PIXELS = 6

        # subtract the pixels of the size-1 squares
        pixels -= (self.size - 1) * self.median_square_width

        # subtrackt the pixels consumed by dilating the edges
        pixels -= (self.size - 1) * DILATION_PIXELS

        self.black_border_width = int(pixels/(self.size - 1))

        if self.debug:
            log.warning("get_black_border_width: top %s, bottom %s, left %s, right %s, pixesl %s (%s), median_square_width %d, black_border_width %s" %
                (self.top, self.bottom, self.left, self.right, pixels, pixels_desc, self.median_square_width, self.black_border_width))

    def sanity_check_results(self, contours, debug=False):

        # Verify we found the correct number of squares
        num_squares = len(contours)
        needed_squares = self.size * self.size

        if num_squares < needed_squares:
            log.debug("sanity False: num_squares %d < needed_squares %d" % (num_squares, needed_squares))
            return False

        elif num_squares < needed_squares:
            # This scenario will need some work so exit here so we notice it
            log.warning("sanity False: num_squares %d > needed_squares %d" % (num_squares, needed_squares))
            sys.exit(1)
            return False

        # Verify each row/col has the same number of neighbors
        req_neighbors = self.size - 1

        for con in contours:
            (row_neighbors, row_square_neighbors, col_neighbors, col_square_neighbors) =\
                self.get_contour_neighbors(contours, con)

            if row_neighbors != req_neighbors:
                log.debug("%s sanity False: row_neighbors %d != req_neighbors %s" % (con, row_neighbors, req_neighbors))
                return False

            if col_neighbors != req_neighbors:
                log.debug("%s sanity False: col_neighbors %d != req_neighbors %s" % (con, col_neighbors, req_neighbors))
                return False

        log.debug("%s sanity True" % con)
        return True

    def get_mean_row_col_for_index(self, col_index, row_index):
        total_X = 0
        total_prev_X = 0
        total_next_X = 0

        total_Y = 0
        total_prev_Y = 0
        total_next_Y = 0

        candidates_X = 0
        candidates_prev_X = 0
        candidates_next_X = 0

        candidates_Y = 0
        candidates_prev_Y = 0
        candidates_next_Y = 0

        for con in self.candidates:
            if con.col_index == col_index - 1:
                total_prev_X += con.cX
                candidates_prev_X += 1

            elif con.col_index == col_index:
                total_X += con.cX
                candidates_X += 1

            elif con.col_index == col_index + 1:
                total_next_X += con.cX
                candidates_next_X += 1

            if con.row_index == row_index - 1:
                total_prev_Y += con.cY
                candidates_prev_Y += 1

            elif con.row_index == row_index:
                total_Y += con.cY
                candidates_Y += 1

            elif con.row_index == row_index - 1:
                total_next_Y += con.cY
                candidates_next_Y += 1

        if candidates_X:
            mean_X = int(total_X/candidates_X)

            if self.debug:
                log.info("get_mean_row_col_for_index: col_index %d, total_X %d, candidates_X %d, mean_X %d" % (col_index, total_X, candidates_X, mean_X))

        elif candidates_prev_X:
            mean_X = int(total_prev_X/candidates_prev_X) + self.median_square_width + self.black_border_width

            if self.debug:
                log.info("get_mean_row_col_for_index: col_index %d, total_prev_X %d, candidates_prev_X %d, mean_X %d" % (col_index, total_prev_X, candidates_prev_X, mean_X))

        elif candidates_next_X:
            mean_X = int(total_next_X/candidates_next_X) - self.median_square_width - self.black_border_width

            if self.debug:
                log.info("get_mean_row_col_for_index: col_index %d, total_next_X %d, candidates_next_X %d, mean_X %d" % (col_index, total_next_X, candidates_next_X, mean_X))

        else:
            assert candidates_X, "candidates_X is %s, it cannot be zero" % candidates_X

        if candidates_Y:
            mean_Y = int(total_Y/candidates_Y)

            if self.debug:
                log.info("get_mean_row_col_for_index: col_index %d, total_Y %d, candidates_Y %d, mean_Y %d" % (col_index, total_Y, candidates_Y, mean_Y))

        elif candidates_prev_Y:
            mean_Y = int(total_prev_Y/candidates_prev_Y) + self.median_square_width + self.black_border_width

            if self.debug:
                log.info("get_mean_row_col_for_index: col_index %d, total_prev_Y %d, candidates_prev_Y %d, mean_Y %d" % (col_index, total_prev_Y, candidates_prev_Y, mean_Y))

        elif candidates_next_Y:
            mean_Y = int(total_next_Y/candidates_next_Y) - self.median_square_width - self.black_border_width

            if self.debug:
                log.info("get_mean_row_col_for_index: col_index %d, total_next_Y %d, candidates_next_Y %d, mean_Y %d" % (col_index, total_next_Y, candidates_next_Y, mean_Y))

        else:
            assert candidates_Y, "candidates_Y is %s, it cannot be zero" % candidates_Y

        return (mean_X, mean_Y)

    def find_missing_squares(self, webcam):

        # It is better if we actually locate all the squares, this is doable with
        # 4x4x4 and smaller but for larger than that there are so many squares it
        # becomes difficult to find all of them in a single frame.
        if webcam and self.size <= 4:
            return []

        # How many squares are missing?
        missing_count = (self.size * self.size) - len(self.candidates)

        if missing_count <= 0:
            if webcam:
                return []
            else:
                assert False, "%dx%dx%d missing_count is %d, we should not be here" % (self.size, self.size, self.size, missing_count)

        if self.debug:
            log.info("find_missing_squares: size %d, missing %d squares" % (self.size, missing_count))

        needed = []
        con_by_row_col_index = {}

        # ID which row and col each candidate contour belongs to
        for con in self.candidates:
            self.set_contour_row_col_index(con)

            if (con.col_index, con.row_index) in con_by_row_col_index:
                assert False, "Found multiple contours for (%d, %d)" % (con.col_index, con.row_index)
            else:
                con_by_row_col_index[(con.col_index, con.row_index)] = con

        if self.debug:
            log.info("find_missing_squares: con_by_row_col_index\n%s" % pformat(con_by_row_col_index))

        # Build a list of the row/col indexes where we need a contour
        for col_index in range(self.size):
            for row_index in range(self.size):
                if (col_index, row_index) not in con_by_row_col_index:
                    needed.append((col_index, row_index))

        if self.debug:
            log.info("find_missing_squares: missing_count %d, needed %s" % (missing_count, pformat(needed)))

        if len(needed) != missing_count:
            if webcam:
                return []
            else:
                raise Exception("missing_count is %d but needed has %d:\n%s" % (missing_count, len(needed), pformat(needed)))

        # For each of 'needed', create a CustomContour() object at the coordinates
        # where we need a contour. This will be a very small square contour but that
        # is all we need.
        index = len(self.contours_by_index.keys()) + 1
        missing = []

        for (col_index, row_index) in needed:
            (missing_X, missing_Y) = self.get_mean_row_col_for_index(col_index, row_index)

            if self.debug:
                log.info("find_missing_squares: contour (%d, %d), coordinates(%d, %d)\n" % (col_index, row_index, missing_X, missing_Y))

            missing_size = 5
            missing_left = missing_X - missing_size
            missing_right = missing_X + missing_size
            missing_top = missing_Y - missing_size
            missing_bottom = missing_Y + missing_size

            missing_con = np.array([[[missing_left, missing_top],
                                     [missing_right,missing_top],
                                     [missing_right, missing_bottom],
                                     [missing_left, missing_bottom]
                                  ]], dtype=np.int32)

            #log.info("missing_con:\n%s\n" % pformat(missing_con))
            con = CustomContour(self, index, missing_con, None, self.debug)
            missing.append(con)
            index += 1

        return missing

    def analyze(self, webcam, gamma_value=1.5):
        assert self.image is not None, "self.image is None"
        (self.img_height, self.img_width) = self.image.shape[:2]
        self.img_area = int(self.img_height * self.img_width)
        self.display_candidates(self.image, "00 original (%s x %x)" % (self.img_height, self.img_width))

        # Removing noise helps a TON with edge detection
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        #self.display_candidates(gray, "09 gray")

        # dwalton this is probably too expensive for --webcam mode...test it
        if webcam:
            nonoise = gray.copy()
        else:
            nonoise = cv2.fastNlMeansDenoising(gray, 10, 10, 7, 21)
            self.display_candidates(nonoise, "10 removed noise")

        # canny to find the edges
        canny = cv2.Canny(nonoise, 10, 30)
        self.display_candidates(canny, "20 canny")

        # dilate the image to make the edge lines thicker
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(canny, kernel, iterations=2)
        self.display_candidates(dilated, "30 dilated")

        try:
            (_, contours, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        except ValueError:
            (contours, hierarchy) = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        self.candidates = []

        if hierarchy is None:
            if webcam:
                return False
            else:
                log.warning("No hierarchy")
                raise Exception("Unable to extract image from %s" % self.name)

        hierarchy = hierarchy[0]

        index = 0
        for component in zip(contours, hierarchy):
            con = CustomContour(self, index, component[0], component[1], self.debug)
            self.contours_by_index[index] = con

            if con.area > 30 and con.cX is not None:
                self.candidates.append(con)
            index += 1


        # Throw away the contours that do not look like squares
        self.display_candidates(self.image, "40 pre non-squares removal #1")

        if self.remove_non_square_candidates():
            self.display_candidates(self.image, "50 post non-squares removal #1")


        # If a contour is more than 25% of the entire image throw it away
        if self.remove_gigantic_candidates(int(self.img_area/4)):
            self.display_candidates(self.image, "60 remove gigantic squares")


        # Sometimes we find a square within a square due to the black space
        # between the cube squares.  Throw away the outside square (it contains
        # the black edge) and keep the inside square.
        if self.remove_square_within_square_candidates():
            self.display_candidates(self.image, "70 post square-within-square removal #1")


        # Find the median square size, we need that in order to find the
        # squares that make up the boundry of the cube
        if not self.get_median_square_area():
            raise CubeNotFound("%s no squares in image" % self.name)


        # Remove contours less than 1/2 the median square size
        if self.remove_dwarf_candidates(int(self.median_square_area/2)):
            self.display_candidates(self.image, "80 remove dwarf squares")

        self.get_median_square_area()


        # Remove contours more than 2x the median square size
        if self.remove_gigantic_candidates(int(self.median_square_area * 2)):
            self.display_candidates(self.image, "90 remove larger squares")

        self.get_median_square_area()

        if not self.get_cube_boundry(False):
            raise CubeNotFound("%s could not find the cube boundry" % self.name)


        # remove all contours that are outside the boundry of the cube
        if self.remove_contours_outside_cube(self.candidates):
            self.display_candidates(self.image, "100 post outside cube removal")


        # Find the cube size (3x3x3, 4x4x4, etc)
        if not self.get_cube_size():
            raise CubeNotFound("%s invalid cube size %sx%sx%s" % (self.name, self.size, self.size, self.size))


        # Now that we know the cube size, re-define the boundry
        if not self.get_cube_boundry(True):
            raise CubeNotFound("%s could not find the cube boundry" % self.name)


        # remove contours outside the boundry
        if self.remove_contours_outside_cube(self.candidates):
            self.display_candidates(self.image, "110 post outside cube removal")


        # Now that we know the median size of each square, go back and
        # remove non-squares one more time
        if self.remove_non_square_candidates(self.median_square_area):
            self.display_candidates(self.image, "120 post non-square-candidates removal")


        # We just removed contours outside the boundry and non-square contours, re-define the boundry
        if not self.get_cube_boundry(True):
            raise CubeNotFound("%s could not find the cube boundry" % self.name)


        # Find the size of the gap between two squares
        self.get_black_border_width()


        if self.sanity_check_results(self.candidates):
            missing = []
        else:
            missing = self.find_missing_squares(webcam)

            if not missing:
                if webcam:
                    return False
                else:
                    log.info("Could not find missing squares needed to create a valid cube")
                    raise Exception("Unable to extract image from %s" % self.name)

            self.candidates.extend(missing)

        self.display_candidates(self.image, "150 Final", missing)

        raw_data = []
        for con in self.sort_by_row_col(deepcopy(self.candidates), self.size):
            # Use the mean value of the contour
            mask = np.zeros(gray.shape, np.uint8)
            cv2.drawContours(mask, [con.contour], 0, 255, -1)
            (mean_blue, mean_green, mean_red, _) = map(int, cv2.mean(self.image, mask = mask))
            raw_data.append((mean_red, mean_green, mean_blue))
        log.debug("squares RGB data\n%s\n" % pformat(raw_data))

        squares_per_side = len(raw_data)
        size = int(math.sqrt(squares_per_side))
        init_square_index = (self.index * squares_per_side) + 1

        square_indexes = []
        for row in range(size):
            square_indexes_for_row = []
            for col in range(size):
                square_indexes_for_row.append(init_square_index + (row * size) + col)
            square_indexes.append(square_indexes_for_row)

        log.debug("%s square_indexes\n%s\n" % (self, pformat(square_indexes)))
        square_indexes = compress_2d_array(square_indexes)
        log.debug("%s square_indexes (final)\n%s\n" % (self, pformat(square_indexes)))

        self.data = {}
        for index in range(squares_per_side):
            square_index = square_indexes[index]
            (red, green, blue) = raw_data[index]
            log.debug("square %d RGB (%d, %d, %d)" % (square_index, red, green, blue))

            # self.data is a dict where the square number (as an int) will be
            # the key and a RGB tuple the value
            self.data[square_index] = (red, green, blue)

        log.debug("")

        # If we made it to here it means we were able to extract the cube from
        # the image with the current gamma setting so no need to look any further
        return True

class RubiksImage(RubiksOpenCV):

    def display_candidates(self, image, desc, missing=[]):
        """
        Used to pop up a window at various stages of the process to show the
        current candidates.  This is only used when debugging else you would
        have a ton of windows popping up all the time.
        """

        if not self.debug:
            return

        log.info("display_candidates() for %s" % desc)

        if self.candidates:
            to_draw = []
            to_draw_square = []
            to_draw_approx = []
            to_draw_missing = []
            to_draw_missing_approx = []

            for con in missing:
                to_draw_missing.append(con.contour)
                to_draw_missing_approx.append(con.approx)

            for con in self.candidates:
                if con in missing:
                    continue

                # Only draw a specific contour
                #if not (con.cX == 188 and con.cY == 93):
                #    continue

                if con.is_square():
                    to_draw_square.append(con.contour)
                    to_draw_approx.append(con.approx)

                else:
                    to_draw.append(con.contour)
                    to_draw_approx.append(con.approx)

            tmp_image = image.copy()
            # cons that are squares are in green
            # for non-squqres the approx is green and contour is blue
            cv2.drawContours(tmp_image, to_draw, -1, (255, 0, 0), 2)
            cv2.drawContours(tmp_image, to_draw_approx, -1, (0, 0, 255), 2)
            cv2.drawContours(tmp_image, to_draw_square, -1, (0, 255, 0), 2)

            if to_draw_missing:
                cv2.drawContours(tmp_image, to_draw_missing, -1, (0, 255, 255), 2)
                cv2.drawContours(tmp_image, to_draw_missing_approx, -1, (255, 255, 0), 2)

            cv2.imshow(desc, tmp_image)
            cv2.waitKey(0)
        else:
            cv2.imshow(desc, image)
            cv2.waitKey(0)

    def analyze_file(self, image_file):
        self.reset()

        # if not os.path.exists(filename):
        #     print("ERROR: %s does not exists" % filename)
        #     sys.exit(1)

        # log.info("Analyze %s" % filename)
        # self.image = cv2.imread(filename)
        self.image = image_file
        return self.analyze(webcam=False)

# if __name__ == '__main__':
#     log.setLevel(logging.DEBUG)
#     index = 0
#     name = "2.png"
#     name = "4.jpg"
#     debug = True
#     debug = False
#     img = cv2.imread(name)
#     rimg = RubiksImage(img,index,name,debug)
#     rimg.analyze_file(img)
#     colors = json.dumps(rimg.data, sort_keys=True)
