diagnosemail = \
    """
    <!DOCTYPE html>
<html lang="en">
    <head>
        <title></title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- <link href="css/style.css" rel="stylesheet"> -->
        <style>
            .content{
                padding: 20px;
                border:10px solid rgb(108, 172, 218)
            }
            .file-content{
                display: inline-block;
            }
            .file-content span{
                display: block;
                text-align:center;
            }
            .file-content a{
                text-decoration: none;
                color:black;
            }
            .result_table{
                width:100%;
                border:0;
                cellspacing:1; 
                cellpadding:0;
                border-collapse: collapse;
            }
            .table-header td{
                color: white;
            }
            table td{
                padding-left: 10px;
            }
            table,table tr th, table tr td {
                border:1px solid #ccc;
                 }
            table tr td a{
                text-decoration: none;
                color:#1b69b6;
            }
            #result-text{
                width: 70%;
                resize: none;
            }
        </style>
    </head>
    <body>
        <div class="content">
            <h4>您好：</h4>
            <h4>&nbsp;&nbsp;&nbsp;&nbsp;针对您最近一次的提交，诊断结果如下：</h4>
            <table class="result_table" >
                <tr class="table-header" style="background-color: gray">
                    <td>名称</td>
                    <td>内容</td>
                    <td>备注</td>
                </tr>
                <tr>
                    <td>project name</td>
                    <td><a href="{project_url}">{project_name}</a></td>
                    <td>&nbsp;</td>
                </tr>
                <tr>
                    <td>commit user</td>
                    <td>{user_name}</td>
                    <td>&nbsp;</td>
                </tr>
                <tr>
                    <td>branch</td>
                    <td>{branch_name}</td>
                    <td>&nbsp;</td>
                </tr>
                <tr>
                    <td>commit</td>
                    <td>{commit_content}</td>
                    <td>&nbsp;</td>
                </tr>
                <tr>
                    <td>commit id</td>
                    <td><a href="{commit_url}">{commit_id}</a></td>
                    <td>&nbsp;</td>
                </tr>
                <tr>
                    <td>commit date</td>
                    <td>{date}</td>
                    <td>&nbsp;</td>
                </tr>
                <tr>
                    <td>diagnose result</td>
                    <td>{result}</td>
                    <td>&nbsp;</td>
                </tr>
            </table>
            <h4 >diagnose detail:</h4>
            <textarea name="" id="result-text" rows="10" readonly>{result_detail}</textarea>
            <h4>更多详情见附件:</h4>
            <div class="file-content">
                <a href="cid:0">
                    <div class="file">
                        <img src="cid:image1" alt="">
                        <span>report.json</span>
                    </div>
                </a>
            </div>
        </div>
    </body>
</html>
    """

if __name__ == "__main__":
    print(diagnosemail)