# coding: utf-8
# Copyright (c) Pymatgen Development Team.
# Distributed under the terms of the MIT License.

"""
Write Prismatic (http://prism-em.com/) input files.
"""


class Prismatic:
    """
    Class to write Prismatic  (http://prism-em.com/) input files.
    This is designed for STEM image simulation.
    """

    def __init__(self, structure, comment="Generated by pymatgen"):
        """
        Args:
            structure: pymatgen Structure
            comment (str): comment
        """
        self.structure = structure
        self.comment = comment

    def to_string(self):
        """
        Returns: Prismatic XYZ file. This is similar to XYZ format
        but has specific requirements for extra fields, headers, etc.
        """

        l = self.structure.lattice
        lines = [self.comment, "{} {} {}".format(l.a, l.b, l.c)]
        for site in self.structure:
            for sp, occu in site.species_and_occu.items():
                lines.append(
                    "{} {} {} {} {} {}".format(
                        sp.Z,
                        site.coords[0],
                        site.coords[1],
                        site.coords[2],
                        occu,
                        site.properties.get("thermal_sigma", 0),
                    )
                )

        lines.append("-1")

        return "\n".join(lines)
