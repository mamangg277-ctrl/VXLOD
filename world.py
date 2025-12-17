from settings import *
from world_objects.chunk import Chunk
from voxel_handler import VoxelHandler


class World:
    def __init__(self, app):
        self.app = app
        self.chunks = [None for _ in range(WORLD_VOL)]
        self.voxels = np.empty([WORLD_VOL, CHUNK_VOL], dtype='uint8')
        self.build_chunks()
        self.build_chunks_mesh()
        self.voxel_handler = VoxelHandler(self)
        self.render_distance_sq = RENDER_DISTANCE * RENDER_DISTANCE

    def update(self):
        self.voxel_handler.update()

    def build_chunks(self):
        for x in range(WORLD_W):
            for y in range(WORLD_H):
                for z in range(WORLD_D):
                    chunk = Chunk(self, position=(x, y, z))

                    chunk_index = x + WORLD_W * z + WORLD_AREA * y
                    self.chunks[chunk_index] = chunk

                    #chnk voxel ditaruh di beda array
                    self.voxels[chunk_index] = chunk.build_voxels()

                    #pointer ke voxel
                    chunk.voxels = self.voxels[chunk_index]

    def build_chunks_mesh(self):
        for chunk in self.chunks:
            chunk.build_mesh()

    def render(self):
        player_chunk_pos = glm.ivec3(self.app.player.position // CHUNK_SIZE)

        for chunk in self.chunks:
            if chunk is None:
                continue
            #hitung jarak
            chunk_dist_sq = glm.distance2(glm.vec3(player_chunk_pos), glm.vec3(chunk.position))
            #hanya render dlm jrk
            if chunk_dist_sq <= self.render_distance_sq:
                chunk.render()