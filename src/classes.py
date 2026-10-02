import pandas as pandas
import matplotlib.pyplot as plt

class BioprocessMonitor:
    def __init__(self, filepath, ph_lims, temperature_lims):
        """
        Utility class used to monitor bioprocesses by
        generating dashboards and summaries.

        Parameters
        ----------
        filepath : str
            Input CSV dataset path.
        ph_lims : tuple[float, float]
            Lower and upper acceptable pH limits.
        temperature_lims : tuple[float, float]
            Lower and upper acceptable temperature limits.
        """
        self.filepath = filepath
        self.ph_low = ph_lims[0]
        self.ph_high = ph_lims[1]
        self.temperature_low = temperature_lims[0]
        self.temperature_high = temperature_lims[1]

    def extract_batch(self, batch_id):
        """
        Extracts data corresponding to a single batch.

        Parameters
        ----------
        batch_id : int
            Batch identifier.

        Returns
        -------
        pandas.DataFrame
            DataFrame containing only rows associated with
            the requested batch.
        """
        df = pandas.read_csv(self.filepath)
        return df[df['batch_id'] == batch_id]


    def optimal_ph_mask(self, df_batch):
        """
        Determines whether each pH measurement falls within
        the acceptable operating range.

        Parameters
        ----------
        df_batch : pandas.DataFrame
            Batch-specific DataFrame.

        Returns
        -------
        array-like of bool
            A mask whereby True indicates that the measurement
            is within the acceptable operating range.
        """
        ph_good = []

        for i in range(df_batch.shape[0]):
            if df_batch.iloc[i,3] >= self.ph_low and df_batch.iloc[i,3] <= self.ph_high:
                ph_good.append(True)
            else:
                ph_good.append(False)

        return ph_good

    def optimal_temperature_mask(self, df_batch):
        """
        Determines whether each temperature measurement falls
        within the acceptable operating range.

        Parameters
        ----------
        df_batch : pandas.DataFrame
            Batch-specific DataFrame.

        Returns
        -------
        array-like of bool
            A mask whereby True indicates that the measurement
            is within the acceptable operating range.
        """
        temp_good = []

        for i in range(df_batch.shape[0]):
            if df_batch.iloc[i, 2] >= self.temperature_low and df_batch.iloc[i, 2] <= self.temperature_high:
                temp_good.append(True)
            else:
                temp_good.append(False)

        return temp_good

    def get_n_batches(self):
        """
        Determines the number of unique batches present
        in the dataset.

        Returns
        -------
        int
            Total number of distinct batch identifiers.
        """
        df = pandas.read_csv(self.filepath)
        return df['batch_id'].nunique()



    def export_dashboard(self, batch_id, filepath):
        """
        Creates and saves a dashboard figure for a single batch.

        Parameters
        ----------
        batch_id : int
            Batch identifier.
        filepath : str
            Output PNG image path.

        Dashboard Requirements
        ----------------------
        Create a 2 × 2 figure containing:

        Top-Left
            Glucose, biomass, and product concentrations versus time.
            - A different color and marker should be used for each substance.

        Top-Right
            Temperature versus time.
            - Measurements within the acceptable temperature range
              should be displayed as green circles.
            - Measurements outside the acceptable temperature range
              should be displayed as red X markers.

        Bottom-Left
            pH versus time.
            - Measurements within the acceptable pH range
              should be displayed as green circles.
            - Measurements outside the acceptable pH range
              should be displayed as red X markers.

        Bottom-Right
            Dissolved oxygen versus time.

        Additional Requirements
        -----------------------
        - Use scatter plots.
        - Add x-axis and y-axis labels.
        - Add legends where appropriate.
        - Apply consistent formatting across all subplots unless
          indicated otherwise.
        - Apply a tick spacing of 6 h on the x-axis for all subplots.
        - Save the figure to the provided filepath.
        - Close the figure after saving.
        """

        df_batch = self.extract_batch(batch_id)
        fig, axes = plt.subplots(2,2,layout="constrained", dpi=400)

        ph_mask = self.optimal_ph_mask(df_batch)
        temp_mask = self.optimal_temperature_mask(df_batch)

        #concentration stuff
        axes[0, 0].scatter(df_batch["time_h"], df_batch["C_glucose_g_L^-1"],color="blue", marker="o", label="Glucose")
        axes[0, 0].scatter(df_batch["time_h"], df_batch["C_biomass_g_L^-1"], color="green", marker="s", label="Biomass")
        axes[0, 0].scatter(df_batch["time_h"], df_batch["C_product_g_L^-1"], color="orange", marker="^", label="Product")

        axes[0,0].set_xlabel("Time [h]")
        axes[0,0].set_ylabel("Concentration [g/L]")
        axes[0,0].legend()

        #temperature stuff
        axes[0, 1].scatter(df_batch.loc[temp_mask, "time_h"], df_batch.loc[temp_mask,"temperature_C"], color="green", marker="o", label="Optimal")
        axes[0, 1].scatter(df_batch.loc[[not x for x in temp_mask], "time_h"], df_batch.loc[[not x for x in temp_mask], "temperature_C"], color="red", marker="x", label="Sub-optimal")

        axes[0, 1].set_xlabel("Time [h]")
        axes[0, 1].set_ylabel("Temperature [Celsius]")
        axes[0, 1].legend()

        #pH stuff
        axes[1, 0].scatter(df_batch.loc[ph_mask, "time_h"], df_batch.loc[ph_mask, "pH"], color="green", marker="o", label="Optimal")
        axes[1, 0].scatter(df_batch.loc[[not x for x in ph_mask], "time_h"], df_batch.loc[[not x for x in ph_mask], "pH"], color="red", marker="x", label="Sub-optimal")

        axes[1, 0].set_xlabel("Time [h]")
        axes[1, 0].set_ylabel("pH")
        axes[1, 0].legend()

        #d.o. stuff
        axes[1, 1].scatter(df_batch["time_h"], df_batch["DO_percent"], color="blue", marker="o", label="D. O. Percent")
        axes[1, 1].set_xlabel("Time [h]")
        axes[1, 1].set_ylabel("Dissolved Oxygen [%]")
        axes[1, 1].legend()

        #adding tickmarks
        for ax in axes.flatten():
            ax.set_xticks(range(int(df_batch["time_h"].min()),int(df_batch["time_h"].max()) + 1,6))

        plt.savefig(filepath)
        plt.close(fig)


    def export_summary(self, filepath):
        """
        Generates a batch summary table and exports it to a CSV file.

        Parameters
        ----------
        filepath : str
            Output CSV table path.

        Summary Table Columns
        ---------------------
        batch_id
            Batch identifier.

        ph_optimal_percent
            Percentage of measurements in a batch within the
            acceptable pH range, rounded to 2 decimal places.

        temperature_optimal_percent
            Percentage of measurements in a batch within the
            acceptable temperature range, rounded to 2 decimal places.

        C_product_g_L^-1_final
            Final product concentration for the batch.
        """

        df = pandas.read_csv(self.filepath)
        batch_ids = df["batch_id"].unique()

        records = []

        for batch_id in batch_ids:
            df_batch = self.extract_batch(batch_id)

            total_entries = df_batch.shape[0]
            temp_mask = self.optimal_temperature_mask(df_batch)
            ph_mask = self.optimal_ph_mask(df_batch)
            temp_ideal_entries = len(df_batch.loc[temp_mask,"temperature_C"])
            ph_ideal_entries = len(df_batch.loc[ph_mask,"pH"])

            final_c = df_batch["C_product_g_L^-1"].iloc[-1]

            record = (batch_id, round(100*ph_ideal_entries/total_entries, 2), round(100*temp_ideal_entries/total_entries,2), round(final_c,2))
            records.append(record)

        summary = pandas.DataFrame(records, columns=["batch_id", "ph_optimal_percent", "temperature_optimal_percent", "C_product_g_L^-1_final"])
        summary.to_csv(filepath, index=False)
