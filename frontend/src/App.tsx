import {
  Box,
  Button,
  Center,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Grid,
  GridItem,
  Input,
  SimpleGrid,
} from '@chakra-ui/react'
import axios from 'axios'
import { Field, Form, Formik } from 'formik'
import { useEffect, useState } from 'react'

import viteLogo from '/vite.svg'

import reactLogo from './assets/react.svg'

function App() {
  const [count, setCount] = useState(0)
  const [message, setMessage] = useState<string>()
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false)
  const [token, setToken] = useState<string>('')
  useEffect(() => {
    console.log(import.meta.env)
    axios.get('http://' + import.meta.env.APP_DOMAIN + '/hello').then((rsp) => {
      console.log(rsp)
      setMessage(rsp.data['message'])
    })
  }, [])

  function validateName(value: string) {
    let error
    if (!value) {
      error = 'Name is required'
    } else if (value.toLowerCase() !== 'admin') {
      error = "Jeez! You're not a fan 😱"
    }
    return error
  }

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
      <Box p={8}>{message}</Box>
      <Box p={8} maxW="960px" mx="auto">
        {!isAuthenticated ? (
          <SimpleGrid spacing={4}>
            <Formik
              initialValues={{ username: 'Sasuke', password: '' }}
              onSubmit={(values, actions) => {
                console.log(values)
                setTimeout(() => {
                  axios
                    .post('http://' + import.meta.env.APP_DOMAIN + '/login', values, {
                      headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                      },
                    })
                    .then((results) => {
                      console.log('RESULTS: ', results.data)
                      setToken(results.data.access_token)
                      setIsAuthenticated(true)
                      actions.setSubmitting(false)
                    })
                    .catch((err) => {
                      console.error('!!!! ', err)
                    })
                }, 1000)
              }}
            >
              {(props) => (
                <Form>
                  <Field name="username" validate={validateName}>
                    {({ field, form }) => (
                      <FormControl
                        isInvalid={form.errors.username && form.touched.username}
                      >
                        <FormLabel>First name</FormLabel>
                        <Input {...field} placeholder="username" />
                        <FormErrorMessage>{form.errors.username}</FormErrorMessage>
                      </FormControl>
                    )}
                  </Field>
                  <Field name="password">
                    {({ field, form }) => (
                      <FormControl
                        isInvalid={form.errors.password && form.touched.password}
                      >
                        <FormLabel>Password</FormLabel>
                        <Input {...field} placeholder="password" />
                        <FormErrorMessage>{form.errors.password}</FormErrorMessage>
                      </FormControl>
                    )}
                  </Field>
                  <Button
                    mt={4}
                    colorScheme="teal"
                    isLoading={props.isSubmitting}
                    type="submit"
                  >
                    Submit
                  </Button>
                </Form>
              )}
            </Formik>
          </SimpleGrid>
        ) : (
          <SimpleGrid spacing={4}>{token}</SimpleGrid>
        )}
      </Box>
      <Box p={8} maxW="960px" mx="auto">
        <Center>
          abc
          <Button colorScheme="blue" onClick={() => setCount((count) => count + 1)}>
            count is {count}
          </Button>
        </Center>
      </Box>
    </>
  )
}

export default App
