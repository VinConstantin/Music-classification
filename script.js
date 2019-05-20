const MAXQTN = 8;
const MINQTN = 2;
function plusQuantite(id) {
    let val = parseInt($("#" + id).data("quantite"))
    if($("#" + id).data("quantite")<MAXQTN){
        $("#" + id).data("quantite",val+1);   
        $("#" + id).html(val+1);    
    }
}
function moinsQuantite(id) {
    let val = parseInt($("#" + id).data("quantite"))
    if($("#" + id).data("quantite")>MINQTN){
        $("#" + id).data("quantite",val-1);   
        $("#" + id).html(val-1);    
    }
}
function insertCbBtn(row,newRow, i){

    let newCell = newRow.insertCell(i)
    let div = document.createElement("div")
    div.className="input-group"
    div.style.minWidth="120px"

    let cb = document.createElement("input");
    cb.setAttribute("type", "checkbox");  
    cb.className = "form-control cb"
    cb.style.maxWidth = "40px"
    cb.id=`cb${i}`
    div.appendChild(cb)

    let input = document.createElement("input");
    input.className = "form-control"
    input.style.maxHeight = "40px"
    input.value = row==null?"": row.data[0][i];
    input.id=`tb`
    div.appendChild(input)

    newCell.appendChild(div)
}

function lireCsv(){
    document.getElementById("Importer").disabled = true;
    document.getElementById("1").style.display = "none";
    document.getElementById("2").style.display = "block"

    let file = customFile.files[0]
    let nb = 0;
    let length = 0;
    let tableHead = document.getElementById("table").getElementsByTagName('thead')[0];
    let tableBody = document.getElementById("table").getElementsByTagName('tbody')[0];
    let newCell
    let newRow
    Papa.parse(file, {
        step: function(row) {
            nb++
            length = row.data[0].length
            if(nb == 1){
                if(document.getElementById('gridCheck1').checked){
                    newRow = tableHead.insertRow(-1)
                    for(let i = 0; i < length;i++){
                        insertCbBtn(row,newRow, i)
                    }
                }
                else{
                    newRow = tableHead.insertRow(-1)
                    for(let i = 0; i < length;i++){
                        insertCbBtn(null,newRow, i)
                    }
                    newRow = tableBody.insertRow(-1)
                    for(let i = 0; i < length;i++){
                        newCell = newRow.insertCell(i)
                        newCell.innerHTML = row.data[0][i]
                    }
                }
            }
            else{
                newRow = tableBody.insertRow(-1)
                for(let i = 0; i < length;i++){
                    newCell = newRow.insertCell(i)
                    newCell.innerHTML = row.data[0][i]
                }
            }          
        },
        complete: function() {
            console.log("All done!");
        }
    });
    
}
function convertHtmlTableToArray(tableId){
    let array = [];
    let headers = [];
    let tb
    let cb
    $(`#${tableId} thead div`).each(function(index, item) {
        tb = item.querySelector("#tb")
        cb = item.querySelector(".cb")
        if(cb.checked || tb.value === "target")
            headers[index] = tb.value
    });
    $(`#${tableId} tbody tr`).has('td').each(function() {
        let arrayItem = {};
        $('td', $(this)).each(function(index, item) {
            if(headers[index]!=null)
            arrayItem[headers[index]] = $(item).html();
        });
        array.push(arrayItem);
    });
    return array;
}
function sendData(){
    let tableId = `table`
    let array = convertHtmlTableToArray(tableId)
    console.log(array)
}