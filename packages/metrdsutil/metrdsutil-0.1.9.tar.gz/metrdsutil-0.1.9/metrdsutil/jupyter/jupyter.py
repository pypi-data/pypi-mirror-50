def imports():
    """
	imports normally used libraries for exploratory analysis

	return: str
		string of imports to be executed with exec()
	"""
    statements = [
        "import pandas as pd",
        "from IPython.core.display import display,HTML",
        "import matplotlib.pyplot as plt",
    ]
    string = ""
    for i in statements:
        string += i + "\n"
        print(i)
    return string


def plot_config():
    """
	viewing configuration for matplotlib
	"""
    statements = ["plt.rcParams['figure.figsize'] = [14, 7]"]
    string = ""
    for i in statements:
        string += i + "\n"
    return string


def notebook_config(notebook_width=75, hide_lines="collapse"):
    """
	configures viewing options of the jupyter notebook

	parameters:
	-----------
	notebook_width : int
		how wide (in %) the notebook should be
	hide_lines : str
		'collapse' for hiding line in/out, 'show' for showing
	"""
    statements = [
        # hide/show code button
        """
HTML('''<script>
code_show=true; 
function code_toggle() {
 if (code_show){
 $('div.input').hide();
 } else {
 $('div.input').show();
 }
 code_show = !code_show
} 
$( document ).ready(code_toggle);
</script>
<form action="javascript:code_toggle()"><input type="submit" value="Show Code"></form>''')
		""",
        # hiding in/out line output
        """display(HTML('<style>.prompt{width: 0px; min-width: 0px; visibility: """
        + hide_lines
        + """}</style>'))""",
        # width of jupyter notebooks
        'display(HTML("<style>.container { width:'
        + str(notebook_width)
        + '% !important; }</style>"))',
        # setting max n of columns for pandas
        """pd.set_option('display.max_columns', 500)""",
        """pd.set_option('display.width', 250)""",
    ]
    string = ""
    for i in statements:
        string += i + "\n"
    return string
