import Button from "@mui/material/Button";
import { TextField, Container, Paper, Box } from "@mui/material";
import { useState } from "react";
import axios from "axios";

function LandingPage() {
    const [text, setText] = useState("");
    const [result, setResult] = useState("")

    async function handleClick() {
        const result = await axios.post("http://localhost:3203/query", {input: text});
        setResult(result.data)
    }


    return (
        <Container sx= {{height: "100vh", display: "flex", flexDirection: "column"}}>
            <Box sx={{flex: 1, display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center"}}>
                <h1>Welcome to Travel Advisor</h1>
                <p>Get started by asking me for travel suggestions</p>
                {"Server Response: " + JSON.stringify(result)}
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
                <TextField fullWidth placeholder="Ask me travel suggestions" id="fullWidth" sx={{ height: "55px" }} onChange={e => setText(e.target.value)} />
                <Button variant="contained" sx={{ height: "55px"}} onClick={handleClick}>
                    Submit
                </Button>
            </Paper>
        </Container>
    );
}

export default LandingPage;
