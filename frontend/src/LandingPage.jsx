import Button from "@mui/material/Button";
import { TextField, Container, Paper, Box } from "@mui/material";
import { useState } from "react";
import axios from "axios";

function LandingPage() {
    const [text, setText] = useState("");

    async function handleClick() {
        const result = await axios.get("http://localhost:3203/"); 
        console.log(result.data);
        setText(result.data); 
    }

    return (
        <Container sx= {{height: "100vh", display: "flex", flexDirection: "column"}}>
            <Box sx={{flex: 1, display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center"}}>
                <h1>Welcome to Travel Advisor</h1>
                <p>Get started by asking me for travel suggestions</p>
                {text && <p>{text}</p>}
            </Box>
            <Paper
                sx={{
                    position: "fixed",
                    bottom: 20,
                    width: "80%",
                    display: "flex",
                    alignItems: "center",
                    gap: 1,
                    backgroundColor: "white",
                }}
            >
                <TextField fullWidth placeholder="Ask me travel suggestions" id="fullWidth" sx={{ height: "55px" }} />
                <Button variant="contained" sx={{ height: "55px", onClick: {handleClick} }}>
                    Submit
                </Button>
            </Paper>
        </Container>
    );
}

export default LandingPage;
