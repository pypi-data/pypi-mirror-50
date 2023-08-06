#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# Secondary Owner: Mounika Kotha (mounika.kotha@teradata.com)
# 
# Version: 1.1
# Function Version: 1.0
# 
# ################################################################## 

from teradataml.common.wrapper_utils import AnalyticsWrapperUtils
from teradataml.common.utils import UtilFuncs
from teradataml.context.context import *
from teradataml.dataframe.dataframe import DataFrame
from teradataml.common.aed_utils import AedUtils
from teradataml.analytics.analytic_query_generator import AnalyticQueryGenerator
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.constants import TeradataConstants
from teradataml.dataframe.dataframe_utils import DataFrameUtils as df_utils
from teradataml.options.display import display

from teradataml.common.utils import package_deprecation

@package_deprecation('16.20.00.02', 'teradataml.analytics.sqle')
class Unpack:
    
    def __init__(self,
        data = None,
        input_column = None,
        output_columns = None,
        output_datatypes = None,
        delimiter = ",",
        column_length = None,
        regex = "(.*)",
        regex_set = 1,
        exception = False) :
        """
        DESCRIPTION:
            The Unpack function unpacks data from a single packed column into 
            multiple columns. The packed column is composed of multiple virtual 
            columns, which become the output columns. To determine the virtual 
            columns, the function must have either the delimiter that separates 
            them in the packed column or their lengths.
        
        
        PARAMETERS:
            data:
                Required Argument.
                The teradataml DataFrame containing the input attributes.
            
            input_column:
                Required Argument.
                Specifies the name of the input column that contains the packed data.
                Types: str
            
            output_columns:
                Required Argument.
                Specifies the names to give to the output columns, in the order in 
                which the corresponding virtual columns appear in input_column. If you 
                specify fewer output column names than there are in virtual input 
                columns, the function ignores the extra virtual input columns. That 
                is, if the packed data contains x+y virtual columns and the 
                output_columns argument specifies x output column names, the function 
                assigns the names to the first x virtual columns and ignores the 
                remaining y virtual columns.
                Types: str OR list of Strings (str)
            
            output_datatypes:
                Required Argument.
                Specifies the datatypes of the unpacked output columns. Supported 
                output_datatypes are VARCHAR, int, float, TIME, DATE, and 
                TIMESTAMP. If output_datatypes specifies only one value and 
                output_columns specifies multiple columns, then the specified value 
                applies to every output_column. If output_datatypes specifies 
                multiple values, then it must specify a value for each output_column. 
                The nth datatype corresponds to the nth output_column. The function 
                can output only 16 VARCHAR columns.
                Types: str OR list of Strings (str)
            
            delimiter:
                Optional Argument.
                Specifies the delimiter (a string) that separates the virtual 
                columns in the packed data. If the virtual columns are separated
                by a delimiter, then specify the delimiter with this argument; 
                otherwise, specify the column_length argument. Do not specify 
                both this argument and the column_length argument.
                Default Value: ","
                Types: str
            
            column_length:
                Optional Argument.
                Specifies the lengths of the virtual columns; therefore, to use this 
                argument, you must know the length of each virtual column. If 
                column_length specifies only one value and output_columns specifies 
                multiple columns, then the specified value applies to every 
                output_column. If column_length specifies multiple values, then it 
                must specify a value for each output_column. The nth datatype 
                corresponds to the nth output_column. However, the last value in
                column_length can be an asterisk (*), which represents a single 
                virtual column that contains the remaining data. For example, 
                if the first three virtual columns have the lengths 2, 1, and 3, 
                and all remaining data belongs to the fourth virtual column, 
                you can specify column_length ("2", "1", "3", *). If you specify
                this argument, you must omit the delimiter argument.
                Types: str OR list of Strings (str)
            
            regex:
                Optional Argument.
                Specifies a regular expression that describes a row of packed data, 
                enabling the function to find the data values. A row of packed data 
                contains one data value for each virtual column, but the row might 
                also contain other information (such as the virtual column name). In 
                the regex, each data value is enclosed in parentheses. For example, 
                suppose that the packed data has two virtual columns, age and 
                sex, and that one row of packed data is: age:34,sex:male The 
                regex that describes the row is ".*:(.*)". The ".*:" matches the 
                virtual column names, age and sex, and the "(.*)" matches the 
                values, 34 and male. The default regex is "(.*)" which matches 
                the whole string (between delimiters, if any). When applied to 
                the preceding sample row, the default regex causes the function 
                to return "age:34" and "sex:male" as data values. To represent 
                multiple data groups in regex, use multiple pairs of parentheses. 
                By default, the last data group in regex represents the data 
                value (other data groups are assumed to be virtual column names 
                or unwanted data). If a different data group represents the data
                value, specify its group number with the regex_set argument.
                Default Value: "(.*)"
                Types: str
            
            regex_set:
                Optional Argument.
                Specifies the ordinal number of the data group in regex 
                that represents the data value in a virtual column. By default, the 
                last data group in regex represents the data value. For 
                example, suppose that regex is: "([a-zA-Z]*):(.*)" If 
                group number is "1", then "([a-zA-Z]*)" represents the data value. If 
                group number is "2", then "(.*)" represents the data value.
                Default Value: 1
                Types: int
            
            exception:
                Optional Argument.
                Specifies whether the function ignores rows that contain invalid 
                data; that is, continues without outputting them. Which causes the 
                function to fail if it encounters a row with invalid data.
                Default Value: False
                Types: bool
        
        RETURNS:
            Instance of Unpack.
            Output teradataml DataFrames can be accessed using attribute
            references, such as UnpackObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
        
        
        RAISES:
            TeradataMlException
        
        
        EXAMPLES:
            # Load the data to run the example.
            load_example_data("Unpack",["ville_tempdata","ville_tempdata1"])
        
            # Create teradataml DataFrame objects
            ville_tempdata1 = DataFrame.from_table("ville_tempdata1")

            # Execute Unpack function
            unpack_out = Unpack(data=ville_tempdata1,
                                input_column='packed_temp_data',
                                output_columns=['city','state','temp_f'],
                                output_datatypes=['varchar','varchar','real'],
                                column_length=['9','9','4'],
                                regex='(.*)',
                                regex_set=1,
                                exception=True)
            
            # Print the results
            unpack_out.result
        
        """
        self.data  = data 
        self.input_column  = input_column 
        self.output_columns  = output_columns 
        self.output_datatypes  = output_datatypes 
        self.delimiter  = delimiter 
        self.column_length  = column_length 
        self.regex  = regex 
        self.regex_set  = regex_set 
        self.exception  = exception 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, "DataFrame"])
        self.__arg_info_matrix.append(["input_column", self.input_column, False, "str"])
        self.__arg_info_matrix.append(["output_columns", self.output_columns, False, "str"])
        self.__arg_info_matrix.append(["output_datatypes", self.output_datatypes, False, "str"])
        self.__arg_info_matrix.append(["delimiter", self.delimiter, True, "str"])
        self.__arg_info_matrix.append(["column_length", self.column_length, True, "str"])
        self.__arg_info_matrix.append(["regex", self.regex, True, "str"])
        self.__arg_info_matrix.append(["regex_set", self.regex_set, True, "int"])
        self.__arg_info_matrix.append(["exception", self.exception, True, "bool"])
        
        # Perform the function validations
        self.__validate()
        # Generate the ML query
        self.__form_tdml_query()
        # Execute ML query
        self.__execute()
        
    def __validate(self) :
        """
        Function to validate sqlmr function arguments, which verifies missing 
        arguments, input argument and table types. Also processes the 
        argument values.
        """
        
        # Make sure that a non-NULL value has been supplied for all mandatory arguments
        self.__awu._validate_missing_required_arguments(self.__arg_info_matrix)
        
        # Make sure that a non-NULL value has been supplied correct type of argument
        self.__awu._validate_argument_types(self.__arg_info_matrix)
        
        # Check to make sure input table types are strings or data frame objects or of valid type.
        self.__awu._validate_input_table_datatype(self.data, "data", None)
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.input_column, "input_column")
        self.__awu._validate_dataframe_has_argument_columns(self.input_column, "input_column", self.data, "data")
        
        
    def __form_tdml_query(self) :
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        
        # Output table arguments list
        self.__func_output_args_sql_names = []
        self.__func_output_args = []
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        self.__func_other_arg_sql_names.append("TargetColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.input_column,"'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("OutputColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.output_columns,"'"))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        self.__func_other_arg_sql_names.append("OutputDataTypes")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.output_datatypes,"'"))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.delimiter is not None and self.delimiter != ",":
            self.__func_other_arg_sql_names.append("Delimiter")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.delimiter,"'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.column_length is not None:
            self.__func_other_arg_sql_names.append("ColumnLength")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.column_length,"'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.regex is not None and self.regex != "(.*)":
            self.__func_other_arg_sql_names.append("Regex")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.regex,"'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.regex_set is not None and self.regex_set != 1:
            self.__func_other_arg_sql_names.append("RegexSet")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.regex_set,"'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.exception is not None and self.exception != False:
            self.__func_other_arg_sql_names.append("IgnoreInvalid")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.exception,"'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        
        # Declare empty lists to hold input table information.
        self.__func_input_arg_sql_names = []
        self.__func_input_table_view_query = []
        self.__func_input_dataframe_type = []
        self.__func_input_distribution = []
        self.__func_input_partition_by_cols = []
        self.__func_input_order_by_cols = []
        
        # Process data
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("ANY")
        self.__func_input_order_by_cols.append("NA_character_")
        
        function_name = "Unpack"
        # Create instance to generate SQLMR.
        aqg_obj = AnalyticQueryGenerator(function_name 
                ,self.__func_input_arg_sql_names 
                ,self.__func_input_table_view_query 
                ,self.__func_input_dataframe_type 
                ,self.__func_input_distribution 
                ,self.__func_input_partition_by_cols 
                ,self.__func_input_order_by_cols 
                ,self.__func_other_arg_sql_names 
                ,self.__func_other_args 
                ,self.__func_other_arg_json_datatypes 
                ,self.__func_output_args_sql_names 
                ,self.__func_output_args)
        # Invoke call to SQL-MR generation.
        self.sqlmr_query = aqg_obj._gen_sqlmr_select_stmt_sql()
        
        # Print SQL-MR query if requested to do so.
        if display.print_sqlmr_query:
            print(self.sqlmr_query)
        
    def __execute(self) :
        """
        Function to execute SQL-MR queries. 
        Create dataframes for the required SQL-MR outputs.
        """
        # Generate STDOUT table name and add it to the output table list.
        sqlmr_stdout_temp_tablename = UtilFuncs._generate_temp_table_name(prefix = "td_sqlmr_out_", use_default_database = True, gc_on_quit = True, quote=False)
        
        try:
            UtilFuncs._create_view(sqlmr_stdout_temp_tablename, self.sqlmr_query)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_EXEC_SQL_FAILED, str(emsg)), MessageCodes.TDMLDF_EXEC_SQL_FAILED)
        
        # Update output table data frames.
        self._mlresults = []
        self.result = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.result)
        
    def __repr__(self) :
        """
        Returns the string representation for a Unpack class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
