=========
Changelog
=========


* :release:`2.2.0 <2019-06-14>`
* :feature:`-` Object model surrounding table schema and table references.

* :release:`2.1.2 <2019-04-30>`
* :bug:`-` pyspark version is specified in install_requires when it is not required.

* :release:`2.1.1 <2019-04-07>`
* :bug:`-` Writing to bigquery could produce decimaltypes that are not supported by parquet.

* :release:`2.1.0 <2019-02-12>`
* :feature:`-` Add utility function to thread transformation scheduling in pyspark.
* :feature:`-` Add a SparkSession preconfigured for testing on local machine.
* :feature:`-` Add a function to select and rename columns in a single call.
* :feature:`-` Modify BigQuery sanitize type to keep DecimalType, but make the type interoperable between Spark and BigQuery.

* :release:`2.0.0 <2018-08-20>`
* :feature:`-` append to a BigQuery table
* :feature:`-` write to BigQuery keep date and timestamp as native types
* :feature:`-` Sanity check about transforming date to string now keeps time and timezone information.
* :release:`1.0.0 <2018-05-25>`
* :feature:`-` Writing to BigQuery now included. All jobs can now use this lib to write to BigQuery.
