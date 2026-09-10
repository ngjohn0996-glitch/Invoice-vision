import React, {useState, useContext, createContext} from "react"

//ObjectContext----------------------------------------------------------------------------------------
const ObjectContext = createContext()

//pass what value to children_component inside <ObjectContext.Provider></ObjectContext.Provider>
function RefreshProvider({children}){
    const [refresh, setRefresh] = useState(true)

    return(
        <>
            <ObjectContext.Provider value={{refresh, setRefresh}}>
                {children}
            </ObjectContext.Provider>
        </>
    )
}



//use pass value
function RefreshUseContext(){
    return useContext(ObjectContext)
}

export {RefreshProvider, RefreshUseContext}