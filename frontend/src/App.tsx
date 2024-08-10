import { Box, Button, Center, Grid, GridItem } from '@chakra-ui/react'
import { useState } from 'react'

import viteLogo from '/vite.svg'

import reactLogo from './assets/react.svg'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Box p={8} maxW="960px" mx="auto">
        <Grid templateColumns="repeat(2, minmax(300px, 1fr))}">
          <GridItem w="100%" h="100">
            <Center h="100%">
              <a href="https://vitejs.dev" target="_blank">
                <img src={viteLogo} className="logo" alt="Vite logo" />
              </a>
            </Center>
          </GridItem>
          <GridItem w="100%" h="100">
            <Center h="100%">
              <a href="https://react.dev" target="_blank">
                <img src={reactLogo} className="logo react" alt="React logo" />
              </a>
            </Center>
          </GridItem>
        </Grid>
      </Box>
      <Box p={8} maxW="960px" mx="auto">
        <Center>
          <Button colorScheme="blue" onClick={() => setCount((count) => count + 1)}>
            count is {count}
          </Button>
        </Center>
      </Box>
    </>
  )
}

export default App
