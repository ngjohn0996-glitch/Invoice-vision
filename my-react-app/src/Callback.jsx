import api from "./api"
import React, {useState, useEffect, useRef} from "react"
import {useNavigate} from "react-router-dom"
import {RefreshUseContext} from "./Refresh"
import {RememberMeUseContext} from "./RememberMe"

function Callback(){

    const firstTime = useRef(true)   //strict mode, want api.post once only 
    const navigate = useNavigate()
    const [error, setError] = useState("")
    const {refresh, setRefresh} = RefreshUseContext()
    const {rememberMe, setRememberMe} = RememberMeUseContext()

    async function fetch(){
        const queryStringDict = new URLSearchParams(window.location.search)
        const codeValue = queryStringDict.get("code")
        if(!codeValue){
            console.log("No code in query string");
            return
        }

        try{
            const response = await api.post("/token",  {code : codeValue, remember_me : rememberMe}, {
                withCredentials: true
            })   //include cookies operation
            const token = response.data.jwt_token
            sessionStorage.setItem("token", token)  
            navigate('/invoice-automation')
            setRefresh(prev => !prev) 
        }catch(err){
            if (err.response?.data?.detail){
                const dataFailDetail = err.response.data.detail
                console.log(dataFailDetail)
                setError(dataFailDetail)
            }else{
                setError("An unexpecet error occur. Please try again.")
            } 
        }
    }

    useEffect(()=>{
        if (firstTime.current){
            firstTime.current = !firstTime.current
            fetch()
        }
    },[])
    


    return(
        <div>
            <h1>Logging in...</h1>
            {error && <span>{error}</span>} 
        </div>
    )
}

export default Callback