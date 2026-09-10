import api from "./api"
import React, {useState, useEffect, useRef} from "react"
import CryptoJS from "crypto-js"
import {useNavigate} from "react-router-dom"

function Component2(){

    //input---------------------------------------------------------------------------------------------------------
    const [input, setInput] = useState({akaunting_email : "",
                                        akaunting_password : "",
                                        company_name : ""})

    function changeInput(event){
        setInput(previnput => ({ ...previnput , [event.target.id] : event.target.value}))
    }



    //disedit & edit-------------------------------------------------------------------------------------------------
    const [disedit, setDisedit] = useState(true)

    function handleDisedit(event){
        event.preventDefault()
        setDisedit(prev => !prev)

        //when edit, store curdbackendJson(lastsave) & setInput lastsave(curdbackendJson)
        if(disedit === false){
            const secretKey = CryptoJS.enc.Utf8.parse("passfgdfg259hkjh") 
            const encryptedPassword = CryptoJS.AES.encrypt(input.akaunting_password, secretKey, {mode:CryptoJS.mode.ECB, padding:CryptoJS.pad.Pkcs7}).toString()
            const curdbackendJson = {...input, akaunting_password : encryptedPassword}
            localStorage.setItem("akaunting_json", JSON.stringify(curdbackendJson))
            setInput({...curdbackendJson, akaunting_password : "************"})
        }
    }



    //click outside form(disedit, setInput lastsave(curdbackendJson))------------------------------------------------
    const formRef = useRef(null)

    useEffect(()=>{
        function handleClickOutside(event){
            {/*edit && not(formref_html_tag  .contains()/div_or_inner_div_has  click_html_tag)*/}
            if(!disedit && !formRef.current.contains(event.target)){
                setDisedit(true)
                const lastsave = localStorage.getItem("akaunting_json")
                if(lastsave){
                    const dict01 = JSON.parse(lastsave)
                    const mask = {...dict01, akaunting_password : "************"}
                    setInput(mask)
                }
            }
        }
        document.addEventListener('click', handleClickOutside)

        return ()=> {document.removeEventListener('click', handleClickOutside)}
    },[disedit])



    //load lastsave(curdbackendJson)--------------------------------------------------------------------------------
    useEffect(()=>{
        const lastsave = localStorage.getItem("akaunting_json")
        if(lastsave){
            const dict01 = JSON.parse(lastsave)
            const mask = {...dict01, akaunting_password : "************"}
            setInput(mask)
        }

    }, [])



    //object_detection-----------------------------------------------------------------------------------------------
    const navigate = useNavigate()

    const fileRef = useRef(null)
    const [yolopost,setYolopost] = useState([])
    const [yolofetch,setYolofetch] = useState([])

    async function objectDetection(event){
        event.preventDefault()
        const token = sessionStorage.getItem("token")

        //array files >>  dict(formdata)
        const formData = new FormData()
        yolopost.forEach(element =>{
            formData.append("files", element)
        })

        try{
            const response = await api.post('/object_detection',formData,{
                headers:{
                    "Authorization": "Bearer " + token   
                }
            })
            const data = response.data  
            const dataJoined = data.map(element =>{
                return{
                    customer : element["Customer"]?.[0], 
                    due_date : element["Due Date"]?.join(" "),  
                    invoice_num : element["Invoice Num"]?.join(" "),  
                    item01_name : element["Item_01 Name"]?.join(" "),  
                    item01_description : element["Item_01 Description"]?.join(" "),  
                    item01_quantity : element["Item_01 Quantity"]?.join(" ").replace(",", "."),  
                    item01_price : element["Item_01 Price"]?.join(" ").replace(",", "."),
                    item02_name : element["Item_02 Name"]?.join(" "),  
                    item02_description : element["Item_02 Description"]?.join(" "),  
                    item02_quantity : element["Item_02 Quantity"]?.join(" ").replace(",", "."),  
                    item02_price : element["Item_02 Price"]?.join(" ").replace(",", "."),  
                    item03_name : element["Item_03 Name"]?.join(" "),  
                    item03_description : element["Item_03 Description"]?.join(" "),  
                    item03_quantity : element["Item_03 Quantity"]?.join(" ").replace(",", "."),  
                    item03_price : element["Item_03 Price"]?.join(" ").replace(",", ".")
                }
            })
            setYolofetch(dataJoined)
            //clear yolopost's file
            setYolopost([])   
            //clear browser's choose file
            if (fileRef.current){
                fileRef.current.value = ""
            }
        }catch(err){
            if(err.response?.status===401){
                sessionStorage.removeItem("token")   
                navigate('/need-auth')
            }
            else if (err.response?.data?.detail){ 
                const dataFailDetail = err.response.data.detail
                console.log(dataFailDetail)
            }else{
                console.log("An unexpecet error occur. Please try again.")
            }
        }
    }

    function changeYolofetch(event){
        const copyarray = [...yolofetch]
        copyarray[Number(event.target.id)][event.target.name] = event.target.value
        setYolofetch(copyarray)
    }



    //invoice_automation--------------------------------------------------------------------------------------------
    async function invoiceAutomation(event){
        event.preventDefault()
        const token = sessionStorage.getItem("token")

        const data_01 = JSON.parse(localStorage.getItem("akaunting_json")) 
        const data_02 = yolofetch[Number(event.target.id)]
        const field = ["item01_description", "item02_description", "item03_description"]
        field.forEach(element =>{
            if (!data_02[element]){
              delete data_02[element];
            }
        })
        const payload = {data_01, data_02}

        try{
            const result = await api.post("/invoice_automation", payload,{
                headers:{
                    "Authorization": "Bearer " + token   
                }
            })
            console.log(result.data)
            if (result.data.status === "Success"){
                setYolofetch(yolofetch.filter((element, index)=>index !== Number(event.target.id)))
            }
        }catch(err){
            if(err.response?.status===401){
                sessionStorage.removeItem("token")   
                navigate('/need-auth')
            }
            else if (err.response?.data?.detail){ 
                const dataFailDetail = err.response.data.detail
                console.log(dataFailDetail)
            }else{
                console.log("An unexpecet error occur. Please try again.")
            }
        }
    }



    //return--------------------------------------------------------------------------------------------------------
    return(
        <div>
            <a>Sync with akaunting</a><br/>
            {disedit && <span>green dot</span>}
            <form ref={formRef} onSubmit={handleDisedit}>
                <input type="text" placeholder="example@email.com" id= "akaunting_email" value={input.akaunting_email} onChange={changeInput} disabled={disedit}></input>
                <input type="text" placeholder="password123" id= "akaunting_password" value={input.akaunting_password} onChange={changeInput} disabled={disedit}></input>
                <input type="text" placeholder="company123" id= "company_name" value={input.company_name} onChange={changeInput} disabled={disedit}></input>
                <button type="submit">{disedit ? "Edit" : "Save"}</button>
            </form><br/>

            <form onSubmit={objectDetection}>
                <input ref={fileRef} type="file" onChange={(e)=>setYolopost(Array.from(e.target.files))} multiple/>{/*setYolopost array files*/}<br/>
                <button type="submit">Submit</button>
            </form><br/>

            {yolofetch.map((element, index)=>( 
                <form key={index} id={index} onSubmit={invoiceAutomation}>
                    <span>Customer:</span> 
                    <input type="text" id={index} name="customer" value={element.customer} onChange={changeYolofetch}></input>
                    <span>Due date:</span> 
                    <input type="text" id={index} name="due_date" value={element.due_date} onChange={changeYolofetch}></input> 
                    <span>Invoice num:</span>
                    <input type="text" id={index} name="invoice_num" value={element.invoice_num} onChange={changeYolofetch}></input>
                    <span>Item_01 name:</span>
                    <input type="text" id={index} name="item01_name" value={element.item01_name} onChange={changeYolofetch}></input>
                    <span>Item_01 description:</span>
                    <input type="text" id={index} name="item01_description" value={element.item01_description} onChange={changeYolofetch}></input>
                    <span>Item_01 quantity:</span>
                    <input type="text" id={index} name="item01_quantity" value={element.item01_quantity} onChange={changeYolofetch}></input>
                    <span>Item_01 price:</span>
                    <input type="text" id={index} name="item01_price" value={element.item01_price} onChange={changeYolofetch}></input>
                    <span>Item_02 name:</span>
                    <input type="text" id={index} name="item02_name" value={element.item02_name} onChange={changeYolofetch}></input>
                    <span>Item_02 description:</span>
                    <input type="text" id={index} name="item02_description" value={element.item02_description} onChange={changeYolofetch}></input>
                    <span>Item_02 quantity:</span>
                    <input type="text" id={index} name="item02_quantity" value={element.item02_quantity} onChange={changeYolofetch}></input>
                    <span>Item_02 price:</span>
                    <input type="text" id={index} name="item02_price" value={element.item02_price} onChange={changeYolofetch}></input>
                    <span>Item_03 name:</span>
                    <input type="text" id={index} name="item03_name" value={element.item03_name} onChange={changeYolofetch}></input>
                    <span>Item_03 description:</span>
                    <input type="text" id={index} name="item03_description" value={element.item03_description} onChange={changeYolofetch}></input>
                    <span>Item_03 quantity:</span>
                    <input type="text" id={index} name="item03_quantity" value={element.item03_quantity} onChange={changeYolofetch}></input>
                    <span>Item_03 price:</span>
                    <input type="text" id={index} name="item03_price" value={element.item03_price} onChange={changeYolofetch}></input>
                    <button type="submit">Automation</button><br/><br/>
                </form>
            ))}
        </div>
    )
}

export default Component2