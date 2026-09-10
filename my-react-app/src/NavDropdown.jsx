import api from "./api"
import React, {useState, useEffect, useRef} from "react"
import {Link} from "react-router-dom"
import {useNavigate} from "react-router-dom"
import {RefreshUseContext} from "./Refresh"
import {RememberMeUseContext} from "./RememberMe"

function NavDropdown(){

    //no token-------------------------------------------------------------------------------------------------------
    const [hasToken, setHasToken] = useState(() => Boolean(sessionStorage.getItem("token")))



    //dropdown------------------------------------------------------------------------------------------------------
    const [dropDown, setdropDown] = useState(false)
    const myGoogleClient = "http://localhost:8000/login"
    const githubHome = "https://github.com/"



    //close dropdown(click outside li)------------------------------------------------------------------------------
    const liRef = useRef(null)

    useEffect(()=>{
        function handleClickOutside(event){
            {/*dropdown && not(liref_html_tag  .contains()/div_or_inner_div_has  click_html_tag)*/}
            if(dropDown && !liRef.current.contains(event.target)){
                setdropDown(false)
            }
        }
        document.addEventListener('click', handleClickOutside)

        return ()=>{document.removeEventListener('click', handleClickOutside)}
    },[dropDown])



    //remember me---------------------------------------------------------------------------------------------------
    const {rememberMe, setRememberMe} = RememberMeUseContext()



    //has token-----------------------------------------------------------------------------------------------------
    const navigate = useNavigate()

    function handleSignOut(){
        setHasToken(false)
        sessionStorage.removeItem("token")
        navigate('/')
    }



    //user info--------------------------------------------------------------------------------------------------------
    const [picture, setPicture] = useState(null)
    
    async function fetch(){
        const token = sessionStorage.getItem("token")
    
        try{
            const response = await api.get("/userinfo",{
                headers:{
                    "Authorization": "Bearer " + token   
                },
                responseType : "blob"
            })
            const data = response.data
            const imageUrl = URL.createObjectURL(data)
            setPicture(imageUrl)
        }catch(err){
            if(err.response?.status===401){
                setHasToken(false)
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



    //refresh component after login------------------------------------------------------------------------------------
    const {refresh, setRefresh} = RefreshUseContext()

    //refresh cause rerender
    useEffect(()=>{
        setHasToken(Boolean(sessionStorage.getItem("token")))

    }, [refresh])

    //useeffect's mount >> no token >> no api.post, no 401error
    //useeffect's hastoken change >> has token >> api.post
    useEffect(()=>{
        if (hasToken){
            fetch()
        }

    },[hasToken])



    //return-----------------------------------------------------------------------------------------------------------
    return(
        <>
            {!hasToken ?
                <>
                    <li ref={liRef} onClick={()=>setdropDown(!dropDown)}><Link to="/">Login</Link></li>
                    {dropDown && 
                    <div>
                        <a href={myGoogleClient}>Login with google</a><br/>   
                        <a href={githubHome}>Login with github</a><br/>
                        <input type="checkbox" checked={rememberMe} onChange={(e)=>setRememberMe(e.target.checked)} onClick={(e)=>e.stopPropagation()}></input>
                        <span>Remember me</span>
                    </div>
                    }
                </> :

                <>
                    <img src={picture} alt="Profile picture"  ref={liRef} onClick={()=>setdropDown(!dropDown)}></img><br/>
                    {dropDown &&
                    <div>
                        <span onClick={handleSignOut}>Sign out</span>
                    </div>
                    }
                </>
            }
        </>
    )
}

export default NavDropdown