from typing import List, Tuple
import hashlib


class Experiment:
    """Experiment class. Contains the logic for assigning users to groups."""

    def __init__(
            self,
            experiment_id: int,
            groups: Tuple[str] = ("A", "B"),
            group_weights: List[float] = None,
    ):
        self.experiment_id = experiment_id
        self.groups = groups
        self.group_weights = group_weights

        # Define the salt for experiment_id.
        # The salt should be deterministic and unique for each experiment_id.
        self.salt = str(experiment_id)

        # Define the group weights if they are not provided equaly distributed
        # Check input group weights. They must be non-negative and sum to 1.
        if self.group_weights is None:
            self.group_weights = [1 / len(groups) for _ in groups]

        elif sum(self.group_weights) != 1 or any(
                [weight < 0 or weight > 1 for weight in self.group_weights]):
            raise ValueError

    def group(self, click_id: int) -> Tuple[int, str]:
        """Assigns a click to a group.

        Parameters
        ----------
        click_id: int :
            id of the click

        Returns
        -------
        Tuple[int, str] :
            group id and group name
        """

        # Assign the click to a group randomly based on the group weights
        # Return the group id and group name
        value_str = str(click_id) + self.salt
        value = int(hashlib.md5(value_str.encode()).hexdigest(), 16) % 100 / 100

        group_id = 0
        proportion = 1
        for weight, group in sorted(zip(self.group_weights, self.groups), reverse=True):

            if value > proportion - weight:
                group_name = group
                for i in range(len(self.groups)):
                    if group_name == self.groups[i]:
                        group_id = i
                        break
                break

            else:
                proportion -= weight

        return group_id, self.groups[group_id]
