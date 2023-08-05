"""A Protocol object for build assembly. Based on a Design and series of Steps."""

from collections import defaultdict
import logging
from typing import Dict, List, Tuple

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

from .containers import Container, Content, Fridge, Plates, content_id
from .design import Design
from .instructions import Transfer, Temperature, Instruction, to_txt


class Step:
    """A single Step in a Protocol."""

    def __init__(self):
        self.transfers: List[Transfer] = []
        self.temps: List[Temperature] = []
        self.instructions: List[str] = []
        self.inputs: Dict[str, Tuple[Content, float]]

    def execute(self, protocol: "Protocol"):
        """Execute a step on a protocol, mutating containers and instructions."""

        raise NotImplementedError


class Protocol:
    """A Protocol object for assembling a library.

    Arguments:
        name {str} -- the name of the protocol
        design {Design} -- the design specification for the build
    """

    def __init__(self, design: Design, name: str = ""):
        self.name = name  # name of the protocol
        self.design = design  # the design specification
        self.steps: List[Step] = []  # list of steps for this assembly
        self.output: List[SeqRecord] = []

        self.how = design.__name__  # ex: plasmid, combinatorial

        # each of the below is set during a 'run()'
        self.containers: List[Container] = []
        self.instructions: List[Instruction] = []  # assembly instructions

    def add(self, step: Step) -> "Protocol":
        """Add a step to the protocol.

        Arguments:
            step {Step} -- the Step to add to this protocol
        """

        if not isinstance(step, Step):
            raise TypeError

        self.steps.append(step)

        return self

    def run(self) -> "Protocol":
        """Run each step of the protcol. Build up the output records and instructions."""

        # all input records, each start out assigned to a single Fridge source
        records = self.design.get_all_records()
        self.containers = [Fridge(r) for r in records]  # first step, all fridge

        for step in self.steps:
            step.execute(self)

        return self

    @property
    def inputs(self) -> Dict[str, float]:
        """Return a map from protocol inputs to volumes in milliters.

        Returns:
            Dict[str, float] -- key, value map from input name to volume
        """

        # gather all transfers where the source was the Fridge
        id_to_volume: Dict[str, float] = defaultdict(float)
        for instruction in self.instructions:
            if not instruction.transfers:
                continue

            for transfer in instruction.transfers:
                if not isinstance(transfer.src, Fridge):
                    continue

                for content in transfer.src:
                    id_to_volume[content_id(content)] += transfer.volume

        # sort descending by volume
        id_volume_sorted = sorted(
            id_to_volume.items(), key=lambda x: x[1], reverse=True
        )
        return {cid: volume for cid, volume in id_volume_sorted}

    @property
    def outputs(self) -> List[SeqRecord]:
        """Gather the output SeqRecords from the final containers after all steps.

        Returns:
            List[SeqRecord] -- SeqRecords created from applying all steps
        """

        accumulator: List[SeqRecord] = []
        for container in self.containers:
            for content in container:
                if isinstance(content, SeqRecord):
                    accumulator.append(content)
        return accumulator

    def to_fasta(self, filename: str) -> int:
        """Write each output record to a FASTA file.

        Uses `SeqIO.write(records, filename, "fasta")`.

        Arguments:
            filename {str} -- the filename to write the FASTA file to

        Returns:
            int -- the number of records that were written
        """

        self._check_output()
        return SeqIO.write(self.outputs, filename, "fasta")

    def to_genbank(self, filename: str) -> int:
        """Write each output record to a Genbank file.

        Uses `SeqIO.write(records, filename, "genbank")`.

        TODO: add a separate flag for writing one GB per record

        Arguments:
            filename {str} -- the filename to write the Genbanks to

        Returns:
            int -- the number of records that were written
        """

        self._check_output()

        # limit for id is 16 characters https://github.com/biopython/biopython/issues/747
        # shorten ids of those that exceed the limit
        for i, output in enumerate(self.outputs):
            if len(output.id) > 16:
                output.description = output.id
                output.id = "Seq" + str(i + 1)

        return SeqIO.write(self.outputs, filename, "genbank")

    def to_txt(self, filename: str):
        """Write the protocol's instructions to a text file.

        Arguments:
            filename {str} -- the filename of the instructin file
        """

        protocol_txt = to_txt(self.name, self.instructions)
        with open(filename, "w") as instruction_file:
            instruction_file.write(protocol_txt)

    def to_csv(self, filename: str):
        """Write CSV file(s) describing the containers/plates after each step.

        Rows of plates/containers are written in CSV format with each step's
        name as its heading

        Example:
        ```py
        protocol.to_csv('instructions')
        ```

        The `.csv` extension is unnecessary and will be added. For most
        multi-step protocols, this method will write multiple CSV files
        appended with each step's 1-based index.

        Arguments:
            filename {str} -- the name of the CSV(s) to write
        """

        csv = ""
        row = 0
        for instruction in self.instructions:
            if not instruction.transfers:
                continue

            name = instruction.name
            row += 1
            csv += f"{name}:\n" if name else f"Setup step {row}:\n"

            unique_wells = list({t.dest for t in instruction.transfers})
            csv += Plates(unique_wells, show_volume=row == 1).to_csv()

        with open(filename, "w") as csvfile:
            csvfile.write(csv)

    def _check_output(self):
        """Verify that the Protocol has steps and that they have been run.

        If there are no steps, or if there is no list of output Records
        in self.containers, there is nothing to write to a FASTA file.
        """
        if not self.steps and not self.outputs:
            raise RuntimeError(
                """No steps or containers specified in Protocol. Running `run()`"""
            )

        if self.steps and not self.outputs:
            logging.warning(
                """Steps specified but no output containers created. Running `run()`"""
            )
            self.run()

            if not self.outputs:
                raise RuntimeError(
                    """Failed to create valid assemblies after executing all steps."""
                )

    def __str__(self):
        """Return a human readable summary of the protocol.

        The python built in function str calls this. Should output a summary like:

        ```txt
        Combinatorial MoClo
            how: combinatorial
            design: [[15 x SeqRecord] [10 x SeqRecord] [2 x SeqRecord]]
            steps: []
        ```
        """

        name = self.name
        how = f"\thow: {self.how}"
        design = f"\tdesign: {str(self.design)}"

        return "\n".join([name, how, design])

    def __iter__(self):
        """Iterate over the steps in this protocol."""

        return iter(self.steps)

    def __len__(self) -> int:
        """Return the number of steps in this protocol.

        Returns:
            int -- the number of steps
        """

        return len(self.steps)
