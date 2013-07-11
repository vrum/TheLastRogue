import gamepiece


class Tile(object):
    def __init__(self):
        self.game_pieces = {
            gamepiece.GamePieceType.ENTITY: [],
            gamepiece.GamePieceType.ITEM: [],
            gamepiece.GamePieceType.DECORATION: [],
            gamepiece.GamePieceType.TERRAIN: []
        }

    def draw(self, position, is_seen, camera):
        for piece_list in self.__pieces_lists_sorted_on_draw_order():
            for piece in piece_list:
                piece.draw(is_seen, camera)

    def __pieces_lists_sorted_on_draw_order(self):
        piece_lists = self.game_pieces.values()
        non_empty_piece_lists = filter(lambda pl: pl != [], piece_lists)
        lists_sorted_on_draw_order = sorted(non_empty_piece_lists,
                                            key=lambda piece_list:
                                            piece_list[0].draw_order)
        return lists_sorted_on_draw_order

    def get_first_item(self):
        return self.get_first_piece_of_type(gamepiece.GamePieceType.ITEM)

    def get_first_entity(self):
        return self.get_first_piece_of_type(gamepiece.GamePieceType.ENTITY)

    def get_terrain(self):
        return self.get_first_piece_of_type(gamepiece.GamePieceType.TERRAIN)

    def get_first_piece_of_type(self, piece_type):
        if(len(self.game_pieces[piece_type]) < 1):
            return None
        return self.game_pieces[piece_type][0]

    def has_entity(self):
        if(len(self.game_pieces[gamepiece.GamePieceType.ENTITY]) < 1):
            return False
        return True

    def copy(self):
        copy = Tile()
        copy.game_pieces = dict()
        for piece_type, piece_list in self.game_pieces.items():
            copy.game_pieces[piece_type] =\
                [piece.piece_copy() for piece in piece_list]
        return copy
