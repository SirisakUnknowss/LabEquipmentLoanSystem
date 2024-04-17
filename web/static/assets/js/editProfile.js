const idNamePrefix = document.querySelector("#idNamePrefix")
const idBranch = document.querySelector("#id_branch")
const idLevelClass = document.querySelector("#idLevelClass")
const idCategory = document.querySelector("#id_category")
const selectEle = [idNamePrefix, idBranch, idLevelClass, idCategory]
// Iterate over the selected elements
for (var i = 0; i < account.length; i++)
{
    for (var j = 0; j < selectEle[i].length; j++)
    {
        if (account[i] == selectEle[i][j].value)
        {
            console.log(selectEle[i][j])
            selectEle[i][j].selected = true
        }
    }
}
