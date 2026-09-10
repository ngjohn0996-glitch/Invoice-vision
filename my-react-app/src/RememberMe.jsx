import React, {useState, useContext, createContext, useEffect} from "react"

const ObjectContext = createContext()

//pass what value to children_component inside <ObjectContext.Provider></ObjectContext.Provider>
function RememberMeProvider({children}){
    //xx Boolean(sessionStorage.getItem("remember_me"))  >>  Boolean("false") = true
    const [rememberMe, setRememberMe] = useState(() => sessionStorage.getItem("remember_me") === "true")

    //store in storage(when redirect to google_client, component remount & value reset to default)
    useEffect(() => {
        sessionStorage.setItem("remember_me", rememberMe);
    }, [rememberMe])

    return(
        <>
            <ObjectContext.Provider value={{rememberMe, setRememberMe}}>
                {children}
            </ObjectContext.Provider>
        </>
    )
}



function RememberMeUseContext(){
    return useContext(ObjectContext)
}

export {RememberMeProvider, RememberMeUseContext}