import type { NextPage } from 'next'
//import Head from 'next/head'
import { useEffect, useState } from 'react'
import {
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  TableCaption,
  TableContainer,
  Box,
  Heading,
  Spacer,
  Stack
} from '@chakra-ui/react'

interface person {
  username: string,
  wins: number,
  losses: number,
  elo: number,
  id: number,
  rank: number
}

const Home: NextPage = () => {
  const id = 1;
  const [data, setData] = useState<person[]>([]);
  const ranks = (sc: number) => {
    return (
      sc == 1 ? "Grand Master" : sc <= 3 ? "Master" : sc <= 4 ? "Candidate Master" : sc <= 7 ? "Expert" : "Novice"
    )
  }

  useEffect(() => {
    (async () => {
      await fetch(`${process.env.NEXT_PUBLIC_URL}/league/players/${id}/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json; encoding=utf=8",
        },
        body: JSON.stringify({
          password: process.env.NEXT_PUBLIC_PASSWORD,
        }),
      })
        .then((response) => response.json())
        .then((dat) => setData(dat));
    })();
  }, [])

  const Row = ({ username, wins, losses, elo, rank }: person) => (
    <Tr>
      <Td>{username}</Td>
      <Td isNumeric>{wins}</Td>
      <Td isNumeric>{losses}</Td>
      <Td isNumeric>{elo}</Td>
      <Td>{ranks(rank)}</Td>
    </Tr>

  )


  return (
    <Box maxWidth="100%">
      <Stack direction="row">
        <Spacer />
        <Heading pt="5" pb="5" >
          Official Chess Rankings
        </Heading>
        <Spacer />
      </Stack>
      <TableContainer>
        <Table variant='simple'>
          <TableCaption>Official Chess Rankings</TableCaption>
          <Thead>
            <Tr>
              <Th>Name</Th>
              <Th isNumeric>Wins</Th>
              <Th isNumeric>Losses</Th>
              <Th isNumeric>Elo Score</Th>
              <Th>Level</Th>
            </Tr>
          </Thead>
          <Tbody>
            {data.map((point: person) => <Row key={point.username} {...point} />)}
          </Tbody>
        </Table>
      </TableContainer>
    </Box>
  )
}

export default Home
