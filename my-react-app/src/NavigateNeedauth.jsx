import api from "./api"
import React, {useEffect, useRef} from "react"
import {useNavigate} from "react-router-dom"
import {RefreshUseContext} from "./Refresh"

function NavigateNeedauth({children}){

    const firstTime = useRef(true)
    const navigate = useNavigate()
    const {refresh, setRefresh} = RefreshUseContext()

    //if no_token or token_expire, refresh token or navigate need-auth-------------------------------------------
    function isTokenExpired(token){
        const dict01 = JSON.parse(atob(token.split('.')[1]))
        const exp = dict01.exp * 1000
        return Date.now() > exp
    }

    async function refreshTokenOrNavigate(){
        try{
            const response = await api.post("/refresh", {}, {
                withCredentials: true
            })   
            const token = response.data.jwt_token
            sessionStorage.setItem("token", token)  
            setRefresh(prev => !prev) 
        }catch(err){
            if (err.response?.data?.detail){
                const dataFailDetail = err.response.data.detail
                console.log(dataFailDetail)
            }else{
                console.log("An unexpecet error occur. Please try again.")
            }
            //run after if statement
            navigate('/need-auth')
        }
    }

    useEffect(()=>{
        if (firstTime.current){
            firstTime.current = !firstTime.current
            const token = sessionStorage.getItem("token")
            if (!token || isTokenExpired(token)){
                refreshTokenOrNavigate()
            } 
        }

    }, [])



    //return parent_component & return children_component(component inside <NavigateNeedauth></NavigateNeedauth>)
    return(
        <>
            {children}
        </>
    )
}

export default NavigateNeedauth