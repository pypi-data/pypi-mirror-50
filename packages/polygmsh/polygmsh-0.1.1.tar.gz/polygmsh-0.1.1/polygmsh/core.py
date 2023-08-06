import time
from os.path import dirname, join
import sys
import subprocess
import geoscr
import click


def cubes(nx, ny, nz):
    geom = geoscr.built_in.Geometry()

    points = [[[
        geom.add_point([x, y, z])
        for z in range(nz + 1)]
        for y in range(ny + 1)]
        for x in range(nx + 1)]

    lines = [[[[
        geom.add_line(points[x][y][z], points[x + 1][y][z]) if x != nx else None,
        geom.add_line(points[x][y][z], points[x][y + 1][z]) if y != ny else None,
        geom.add_line(points[x][y][z], points[x][y][z + 1]) if z != nz else None]
        for z in range(nz + 1)]
        for y in range(ny + 1)]
        for x in range(nx + 1)]

    surfaces = [
        [[[
              geom.add_plane_surface(geom.add_line_loop([
                  lines[x][y][z][1],
                  lines[x][y + 1][z][2],
                  -lines[x][y][z + 1][1],
                  -lines[x][y][z][2]
              ])) if y != ny and z != nz else None,
              geom.add_plane_surface(geom.add_line_loop([
                  lines[x][y][z][2],
                  lines[x][y][z + 1][0],
                  -lines[x + 1][y][z][2],
                  -lines[x][y][z][0]
              ])) if x != nx and z != nz else None,
              geom.add_plane_surface(geom.add_line_loop([
                  lines[x][y][z][0],
                  lines[x + 1][y][z][1],
                  -lines[x][y + 1][z][0],
                  -lines[x][y][z][1]
              ])) if y != ny and x != nx else None
          ] if z != nz or (x != nx and y != ny) else None
          for z in range(nz + 1)
          ] if x != nx or y != ny else None
         for y in range(ny + 1)
         ] for x in range(nx + 1)]

    volumes = [[[
        geom.add_volume(geom.add_surface_loop([
            surfaces[x][y][z][0],  # should be inverted but it works...
            surfaces[x][y][z][1],  # should be inverted but it works...
            surfaces[x][y][z][2],  # should be inverted but it works...
            surfaces[x + 1][y][z][0],
            surfaces[x][y + 1][z][1],
            surfaces[x][y][z + 1][2]]))
        for z in range(nz)]
        for y in range(ny)]
        for x in range(nx)]

    return geom


def cli():
    if sys.argv[1] == "set-gmsh-path":
        set_gmsh_path(sys.argv[2])
        return

    try:
        with open(join(dirname(__file__), "gmsh-path.pth"), "r") as f:
            sys.path.insert(0, f.readline())
    except FileNotFoundError:
        pass

    genmesh()


@click.command()
@click.argument("nx", type=click.INT)
@click.argument("ny", type=click.INT)
@click.argument("nz", type=click.INT)
@click.option("-o", "--out", type=click.STRING, default="mesh.key",
              help="Output file name.\n"
                   "Possible file types: msh1, msh2, msh22, msh3, msh4, msh40, msh41, msh, "
                   "unv, vtk, wrl, mail, stl, p3d, mesh, bdf, cgns, med, diff, ir3, inp, "
                   "ply2, celum, su2, x3d, dat, neu, m, key.")
@click.option("-p", "--preflen", type=click.FLOAT, help="Preferred tetrahedron edge length.")
@click.option("--nthrs", type=click.INT, help="Threads number.")
def genmesh(nx, ny, nz, out, preflen, nthrs):
    gen_start = time.time()
    geom = cubes(nx, ny, nz)
    gen_time = time.time() - gen_start
    print("Done generating geometry ({0:.3f} s)".format(gen_time))

    with open("cubes.geo", 'w') as f:
        f.write(geom.get_code())

    subprocess.run(
        ["gmsh",
         "-open", "cubes.geo",
         "-o", out,
         "-3",
         "-algo", "del3d",
         "-smooth", "10",
         "-optimize_netgen"]
        + (["-nt", str(nthrs)] if nthrs is not None else [])
        + (["-clmin", str(preflen),
            "-clmax", str(preflen)] if preflen is not None else []))


def set_gmsh_path(gmshpath):
    with open(join(dirname(__file__), "gmsh-path.pth"), "w") as f:
        f.write(gmshpath)
    print("Done saving gmsh path.")
