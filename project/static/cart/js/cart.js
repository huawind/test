$(document).ready(function(){
    //修改购物车
    var addShoppings = document.getElementsByClassName("addShopping")
    var subShoppings = document.getElementsByClassName("subShopping")
    var jiage= document.getElementById("ccc")
    console.log(jiage)
    // jiage.innerHTML = "总价"+100

    for (var i = 0; i < addShoppings.length; i++){
        addShopping = addShoppings[i]
        addShopping.addEventListener("click", function(){
            pid = this.getAttribute("ga")
            $.post("/changecart/0/",{"productid":pid}, function(data){
                if (data.status == "success"){
                    //添加成功，把中间的span的innerHTML变成当前的数量
                    document.getElementById(pid).innerHTML = data.data
                    document.getElementById(pid+"price").innerHTML = data.price
                }
            })
        })
    }


    for (var i = 0; i < subShoppings.length; i++){
        subShopping = subShoppings[i]
        subShopping.addEventListener("click", function(){
            pid = this.getAttribute("ga")
            $.post("/changecart/1/",{"productid":pid}, function(data){
                if (data.status == "success"){
                    //添加成功，把中间的span的innerHTML变成当前的数量
                    document.getElementById(pid).innerHTML = data.data
                    document.getElementById(pid+"price").innerHTML = data.price
                    if(data.data == 0) {
                        //window.location.href = "http://127.0.0.1:8001/cart/"
                        var li = document.getElementById(pid+"li")
                        li.parentNode.removeChild(li)
                    }
                }
            })
        })
    }



    var ischoses = document.getElementsByClassName("ischose")
    for (var j = 0; j < ischoses.length; j++){
        ischose = ischoses[j]
        ischose.addEventListener("click", function(){
            pid = this.getAttribute("goodsid")
            $.post("/changecart/2/", {"productid":pid}, function(data){
                if (data.status == "success"){
                    //window.location.href = "http://127.0.0.1:8001/cart/"
                    var s = document.getElementById(pid+"a")
                    console.log(s)
                    s.innerHTML = data.data
                    console.log(data.data)

                }
            })
        },false)
    }
    var ok = document.getElementById("ok")
    ok.addEventListener("click", function(){
        var f = confirm("是否确认下单？")
        if (f){
            $.post("/saveorder/", function(data){
                if (data.status = "success"){
                    window.location.href = "http://127.0.0.1:8008/cart/"

                }
            })
        }
    },false)
})