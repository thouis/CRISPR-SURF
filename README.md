# CRISPR-SURF

CRISPR-SURF (**S**creening of **U**ncharacterized **R**egion **F**unction) is an exploratory and interactive computational framework for the design and analysis of CRISPR-Cas, CRISPRi, and CRISPRa tiling screens.

CRISPR-SURF is available as a user-friendly, open-source software and can be used interactively as a web application at [crisprsurf.pinellolab.org](http://crisprsurf.pinellolab.org/) or as a stand-alone command-line tool with Docker [https://github.com/pinellolab/CRISPR-SURF](https://github.com/pinellolab/CRISPR-SURF).

## Installation with Docker

With Docker, no installation is required - the only dependence is Docker itself. Users will not need to deal with installation and configuration issues. Docker will do all the dirty work for you!

Docker can be downloaded freely here: [https://store.docker.com/search?offering=community&type=edition](https://store.docker.com/search?offering=community&type=edition)

To get a local copy of CRISPR-SURF, simply execute the following command:
* ```docker pull pinellolab/crisprsurf```

## CRISPR-SURF Design

The CRISPR-SURF Design script allows users to design sgRNAs for their CRISPR tiling screen. Run CRISPR-SURF Design in the terminal with the command:

```
docker run -v $PWD:$PWD -w $PWD pinellolab/crisprsurf SURF_design [options]
```

Users can specify the following options:
```
-bed, --bed
      Input bed file to design tiling sgRNAs. (Default: None)
-genome, --genome
      Input genome 2bit file. (Default: None)
-pams, --pams
      Specification of different CRISPR PAMs (i.e. [ATCG]GG, TTT[ACG]). This can be a list with multiple PAMs separated by spaces. (Default: None)
-orient, --orientations
      Orientation of spacer relative to PAM. This must match the length of the -pams option as an orientation must be specified for each PAM. Multiple orientations are separated by spaces. (left, right | Default: None)
-guide_l, --guide_length
      Length of the sgRNA to design. (Default: 20)
-g_constraint, --g_constraint
      Constraint forcing the 5' sgRNA bp to be G base. (true, false | Default: false)
-out, --out_dir
      Name of output directory. (Default: .)
```

**Example Command-Line Run**

```
docker run -v $PWD:$PWD -w $PWD pinellolab/crisprsurf SURF_design -bed /PATH/TO/BED -genome /PATH/TO/2BIT_GENOME -pams [ATCG]GG TTT[ACG] -orient left right -guide_l 20 -g_constraint false -out example_run
```

**Running Cas-OFFinder**

The off-targets of the designed sgRNAs can be enumerated with Cas-OFFinder by isolating the 4th column in the CRISPR-SURF Design output file, ```SURF_designed_sgRNAs.csv```. Instructions on running Cas-OFFinder can be found here: http://www.rgenome.net/cas-offinder/portable

## CRISPR-SURF Count

The CRISPR-SURF Count script generates a required input file, ```sgRNAs_summary_table.csv```, for both the CRISPR-SURF interactive website and command-line interface. Run CRISPR-SURF Count in the terminal with the command:

```
docker run -v $PWD:$PWD -w $PWD pinellolab/crisprsurf SURF_count [options]
```

Users can specify the following options:
```
-f, --sgRNA_library  
      Input sgRNA library file. Formatting specified below. (Default: None)
-control_fastqs, --control_fastqs
      List of control FASTQs with sgRNA counts prior to selection. Example: rep1_control.fastq rep2_control.fastq rep3_control.fastq (Default: None)
-sample_fastqs, --sample_fastqs
      List of sample FASTQs with sgRNA counts following selection. Example: rep1_sample.fastq rep2_sample.fastq rep3_sample.fastq (Default: None)
-nuclease, --nuclease
      Nuclease used in the CRISPR tiling screen experiment. This information is used to determine the cleavage index if indels are specified as the perturbation. (cas9, cpf1 | Default: cas9)
-pert, --perturbation
      Perturbation type used in the CRISPR tiling screen experiment. This information is used to determine the perturbation index for a given sgRNA. (indel, crispri, crispra | Default: indel)
-norm, --normalization
      Normalization method between sequencing libraries. (none, median, total | Default: median)
-count_method, --count_method
      Counting method for sgRNA counting from FASTQ. The tracrRNA option aligns a consensus sequence directly downstream of the sgRNA. The index option uses provided indices to grab sgRNA sequence from read. (tracrRNA, index | Default: tracrRNA)
-tracrRNA, --tracrRNA
      If -count_method == tracrRNA. The consensus tracrRNA sequence directly downstream of the sgRNA for counting from FASTQ. (Default: GTTTTAG)
-sgRNA_index, --sgRNA_index
      If -count_method == index. The sgRNA start and stop indices (0-index) within the FASTQ reads. Example: 0 20 (Default: 0 20)
-count_min, --count_minimum
      The minimum number of counts for a given sgRNA in each control sample. (Default: 50)
-dropout, --dropout_penalty
      The dropout penalty removes sgRNAs that have a 0 count in any of the control/sample replicates. (Default: True)
-TTTT, --TTTT_penalty
      The TTTT penalty removes sgRNAs that have a homopolymer stretch of Ts >= 4. (Default: True)
-sgRNA_length, --sgRNA_length
      Length of sgRNAs used in the CRISPR tiling screen experiment. This must match the sgRNA length provided in the sgRNA library file. (Default: 20)
-reverse, --reverse_score
      Reverse the enrichment score. Generally applied to depletion screens where a positive score is associated with depletion of a sgRNA. (Default: False)
-out_dir, --out_directory
      The output directory for CRISPR-SURF counts. (Default: .)
```

To start, you will need one of the following:

* **Option (1)** sgRNA Library File with FASTQs
* **Option (2)** sgRNA Library File with counts

**Option (1)**:
----------------
sgRNA Library File Format Example (.CSV):

| Chr           | Start         | Stop          | sgRNA_Sequence       | Strand | sgRNA_Type       |
| ------------- | ------------- | ------------- | -------------------- | ------ | ---------------- |
| chr2          | 60717499      | 60717519      | AGCTCTGGAATGATGGCTTA | -      | observation      |
| chr2          | 60717506      | 60717526      | ATTGTGGAGCTCTGGAATGA | +      | observation      |
| chr2          | 60717514      | 60717534      | GGAGTTGGATTGTGGAGCTC | +      | observation      |
| chr2          | 60717522      | 60717542      | AGAAAATTGGAGTTGGATTG | -      | negative_control |
| chr2          | 60717529      | 60717549      | CTGGAATAGAAAATTGGAGT | +      | positive_control |

Required Column Names:
* **Chr** - Chromosome
* **Start** - sgRNA Start Genomic Coordinate
* **Stop** - sgRNA Start Genomic Coordinate
* **sgRNA_Sequence** - sgRNA sequence not including PAM sequence
* **Strand** - Targeting strand of the sgRNA
* **sgRNA_Type** - Label for sgRNA type (observation, negative_control, positive_control)

**Example Command-Line Run on Canver et al. 2015**

The following command will run CRISPR-SURF Count for Option (1) on provided example data:
```
docker run -v $PWD:$PWD -w $PWD pinellolab/crisprsurf SURF_count -f /SURF/command_line/exampleDataset/sgRNA_library_file.csv -control_fastqs /SURF/command_line/exampleDataset/rep1_neg.fastq.gz /SURF/command_line/exampleDataset/rep2_neg.fastq.gz -sample_fastqs /SURF/command_line/exampleDataset/rep1_pos.fastq.gz /SURF/command_line/exampleDataset/rep2_pos.fastq.gz -nuclease cas9 -pert indel
```

**Run CRISPR-SURF Count Option (1) Yourself**

Place the sgRNA library file and FASTQs in the same directory. The control FASTQs represent the sgRNA distribution prior to selection, while the sample FASTQs represent the sgRNA distribution following selection. Assuming the sgRNA library file is named ```sgRNA_library_file.csv```, the FASTQs (2 replicates) are named ```rep1_control.fastq```, ```rep2_control.fastq```, ```rep1_sample.fastq```, ```rep2_sample.fastq```, and it's a CRISPR-Cas9 tiling screen, the command-line call would look like:

``` 
docker run -v $PWD:$PWD -w $PWD pinellolab/crisprsurf SURF_count -f sgRNA_library_file.csv -control_fastqs rep1_control.fastq rep2_control.fastq -sample_fastqs rep1_sample.fastq rep2_sample.fastq -nuclease cas9 -pert indel
```

Simply change ```-pert indel``` to ```-pert crispri``` or ```-pert crispra``` for CRISPRi and CRISPRa screens, respectively.

**IMPORTANT:** The number of control FASTQs must equal the number of sample FASTQs. If a single control FASTQ (i.e. plasmid count) is used for multiple sample FASTQs, just enumerate the ```-control_fastqs``` option with the same single control FASTQ.

**Option (2)**:
----------------
sgRNA Library File Format Example (.CSV):

| Chr           | Start         | Stop          | sgRNA_Sequence       | Strand | sgRNA_Type       | Replicate1_Control_Count | Replicate2_Control_Count | Replicate1_Sample_Count | Replicate2_Sample_Count |
| ------------- | ------------- | ------------- | -------------------- | ------ | ---------------- | ------------------------ | ------------------------ | ----------------------- | ----------------------- |
| chr2          | 60717499      | 60717519      | AGCTCTGGAATGATGGCTTA | -      | observation      | 322                      | 615                      | 131                     | 403                     |
| chr2          | 60717506      | 60717526      | ATTGTGGAGCTCTGGAATGA | +      | observation      | 365                      | 812                      | 448                     | 227                     |
| chr2          | 60717514      | 60717534      | GGAGTTGGATTGTGGAGCTC | +      | observation      | 86                       | 169                      | 13                      | 129                     |
| chr2          | 60717522      | 60717542      | AGAAAATTGGAGTTGGATTG | -      | negative_control | 1823                     | 381                      | 1923                    | 321                     |
| chr2          | 60717529      | 60717549      | CTGGAATAGAAAATTGGAGT | +      | positive_control | 54                       | 124                      | 355                     | 521                     |

Required Column Names:
* **Chr** - Chromosome
* **Start** - sgRNA Start Genomic Coordinate
* **Stop** - sgRNA Start Genomic Coordinate
* **sgRNA_Sequence** - sgRNA sequence not including PAM sequence
* **Strand** - Targeting strand of the sgRNA
* **sgRNA_Type** - Label for sgRNA type (observation, negative_control, positive_control)
* **Replicate1_Control_Count** - sgRNA Count in Replicate 1 Control FASTQ (pre-selection)
* **Replicate2_Control_Count** - sgRNA Count in Replicate 2 Control FASTQ (pre-selection)
* **Replicate1_Sample_Count** - sgRNA Count in Replicate 1 Sample FASTQ (post-selection)
* **Replicate2_Sample_Count** - sgRNA Count in Replicate 2 Sample FASTQ (post-selection)

**Example Command-Line Run on Canver et al. 2015**

The following command will run CRISPR-SURF Count for Option (2) on provided example data:

```
docker run -v $PWD:$PWD -w $PWD pinellolab/crisprsurf SURF_count -f /SURF/command_line/exampleDataset/sgRNA_library_file_w_counts.csv -nuclease cas9 -pert indel
```

**Run CRISPR-SURF Count Option (2) Yourself**

Go into the directory where the sgRNA library file is located. Assuming the sgRNA library file with counts is named ```sgRNA_library_file_w_counts.csv``` and it's a CRISPR-Cas9 tiling screen, the command-line call would look like:

``` 
docker run -v $PWD:$PWD -w $PWD pinellolab/crisprsurf SURF_count -f sgRNA_library_file_w_counts.csv -nuclease cas9 -pert indel
```

Simply change ```-pert indel``` to ```-pert crispri``` or ```-pert crispra``` for CRISPRi and CRISPRa screens, respectively.

**IMPORTANT:** Additional ReplicateN_Control_Count and ReplicateN_Sample_Count columns can be added depending on the number of replicates used in the experiment. The number of ReplicateN_Control_Count columns must equal ReplicateN_Sample_Count columns. If a single control column (i.e. plasmid count) is used for multiple sample counts, just duplicate the single control column with the appropriate column names.

## CRISPR-SURF Interactive Website

In order to make CRISPR-SURF more user-friendly and accessible, we have created an interactive website: [http://crisprsurf.pinellolab.org](http://crisprsurf.pinellolab.org). The website implements all the features of the CRISPR-SURF command-line tool (except CRISPR-SURF Count) and, in addition, provides interactive and exploratory plots to visualize your CRISPR tiling screen data.

The website offers two functions: 1) Running CRISPR-SURF on data provided by the user and 2) Visualizing CRISPR-SURF analysis on several published data sets, serving as the first database dedicated to CRISPR tiling screen data.

The website can also run on a local machine using the provided Docker image we have created. To run the website on a local machine after the Docker installation, execute the following command from the command line:
* ```docker run -p 9993:9993 pinellolab/crisprsurf SURF_webapp```

After execution of the command, the user will have a local instance of the website accessible at the URL: 
[http://localhost:9993](http://localhost:9993)

## CRISPR-SURF Command-Line Interface

The CRISPR-SURF command-line interface takes ```sgRNAs_summary_table.csv``` (generated from CRISPR-SURF Count) as input. Run the CRISPR-SURF command-line tool in the terminal with the command:

```
docker run -v $PWD:$PWD -w $PWD pinellolab/crisprsurf SURF_deconvolution [options]
```

Users can specify the following options:
```
-f, --sgRNAs_summary_table
      Input sgRNAs summary table. Direct output of CRISPR-SURF Count. (Default: None)
-pert, --perturbation_type
      The CRISPR perturbation type used in the tiling experiment. (cas9, cpf1, crispri, crispra)
-range, --characteristic_perturbation_range (Default: None)
      Characteristic perturbation length. If 0 (default), the --perturbation_type argument will be used to set an appropriate perturbation range. (Default: 0)
-scale, --scale
      Scaling factor to efficiently perform deconvolution with negligible consequences. If 0 (default), the --characteristic_perturbation_range argument will be used to set an appropriate scaling factor. (Default: 0)
-limit, --limit
      Maximum distance between two sgRNAs to perform inference on bp in-between. Sets the boundaries of the gaussian profile to perform efficient deconvolution. If 0 (default), the --perturbation_type argument will be used to set an appropriate limit. (Default: 0)
-avg, --averaging_method
      The averaging method to be performed to combine biological replicates. (mean, median | Default: median)
-sim_type, --simulation_type
      The method of building a null distribution for each smoothed beta score. (negative_control, gaussian, laplace | Default: gaussian)
-sim_n, --simulation_n
      The number of simulations to perform for construction of the null distribution. (Default: 1000)
-lambda_list, --lambda_list
      List of lambdas (regularization parameter) to use during deconvolution step. If 0 (default), the --perturbation_type argument will be used to set a reasonable lambda list. Example: 1 2 3 4 5 6 7 8 9 10. (Default: 0)
-lambda_val, --lambda_val
      The lambda to use to use during deconvolution step. If 0 (default), the --lambda_list argument will be used. (Default: 0)
-corr, --correlation
      The correlation between biological replicates to determine a reasonable lambda for the deconvolution operation. if 0 (default), the --characteristic_perturbation_range argument will be used to set an appropriate correlation.
-genome, --genome
      The genome to be used to create the IGV session file. (hg19, hg38, mm9, mm10, etc. | Default: hg19)
-effect_size, --effect_size
      Effect size to estimate statistical power. (Default: 1)
-padjs, --padj_cutoffs
      List of p-adj. (Benjamini-Hochberg) cut-offs for determining significance of regulatory regions in the CRISPR tiling screen. Example: 0.01 0.05 0.1 0.15. (Default: 0.05)
-rapid, --rapid_mode
      Significance testing can be performed more rapidly with the assumption beta nulls come from same distribution. (Default: False)
-out_dir, --out_directory
      The name of the output directory to place CRISPR-SURF analysis files. (Default: CRISPR_SURF_Analysis_[INSERT TIMESTAMP])
```

**Example Command-Line Run on Canver et al. 2015**

The following command will run CRISPR-SURF analysis on provided example data:
```
docker run -v $PWD:$PWD -w $PWD pinellolab/crisprsurf SURF_deconvolution -f /SURF/command_line/exampleDataset/sgRNAs_summary_table.csv -pert cas9
```

**Run CRISPR-SURF Command-Line Interface (2) Yourself**

Go into the directory where the sgRNAs summary table is located. Assuming the sgRNAs summary table is named                   ```sgRNAs_summary_table.csv``` and it's a CRISPR-Cas9 tiling screen, the command-line call would look like:

```
docker run -v $PWD:$PWD -w $PWD pinellolab/crisprsurf SURF_deconvolution -f sgRNAs_summary_table.csv -pert cas9
```

Simply change ```-pert cas9``` to ```-pert crispri``` or ```-pert crispra``` for CRISPRi and CRISPRa screens, respectively.

## Output Files

**1. sgRNAs_summary_table_updated.csv:** An updated sgRNAs summary table with deconvolution and p-adj. values.

**2. igv_session.xml:** An IGV session for the following tracks
* **raw_scores.bedgraph** - sgRNA enrichment scores
* **deconvolved_scores.bedgraph** - deconvolution beta profile
* **positive_significant_regions.bed** - positive significant regions at set FDR
* **negative_significant_regions.bed** - negative significant regions at set FDR
* **statistical_power.bedgraph** - statistical power track at set effect size and FDR

**3. significant_regions.csv:** List of the significant regions and its associated statistics and supporting sgRNAs.

**4. beta_profile.csv:** Full deconvolution beta profile with associated statistics.

**5. correlation_curve_lambda.csv:** The correlation curve generated for determining lambda.

**6. crispr-surf_parameters.csv:** The CRISPR-SURF analysis parameters used during the analysis session.

**7. crispr-surf.log:** The log file for CRISPR-SURF analysis.
