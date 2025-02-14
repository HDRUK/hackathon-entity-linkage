import { MetaFunction } from "@remix-run/node";
import {
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Checkbox,
  TableSortLabel,
  Link,
  Typography,
} from "@mui/material";
import { useState } from "react";
import { useLoaderData } from "@remix-run/react";
import {
  flexRender,
  getCoreRowModel,
  useReactTable,
  getSortedRowModel,
  ColumnDef,
  SortingState,
} from "@tanstack/react-table";

export const loader = async () => {
  const response = await fetch("http://localhost:8000/find");
  const data = await response.json();
  return data;
};

export const meta: MetaFunction = () => [
  { title: "Automated Entity Linkage" },
  { name: "description", content: "" },
];

interface Option {
  id: number;
  title: string;
  doi?: string;
}

interface DataItem {
  paper: Option;
  dataset: Option;
  score: number;
}

export default function Index() {
  const data = useLoaderData();
  const [rows, setRows] = useState<DataItem[]>(data.data);
  const [checked, setChecked] = useState({});

  const [sorting, setSorting] = useState<SortingState>([
    { id: "score", desc: true },
  ]);

  const columns: ColumnDef<DataItem[]> = [
    {
      accessorFn: (row) => row.source,
      id: "type",
      cell: (info) => <b> {info.getValue()} </b>,
      header: () => <>Source</>,
    },
    {
      accessorFn: (row) => row.paper.title,
      id: "paperTitle",
      cell: (info) => (
        <Link href={info.row.original.paper.doi} target="_blank">
          {info.getValue()}
        </Link>
      ),
      header: () => <>Paper Title</>,
    },
    {
      accessorFn: (row) => row.dataset.title,
      id: "datasetTitle",
      cell: (info) => (
        <Link
          target="_blank"
          href={`https://healthdatagateway.org/dataset/${info.row.original.dataset.id}`}
        >
          {info.getValue()}
        </Link>
      ),
      header: () => <>Dataset Title</>,
    },
    {
      accessorFn: (row) => row.score.toFixed(2),
      id: "score",
      cell: (info) => info.getValue(),
      header: () => <> Score </>,
    },
    {
      id: "approve",
      header: "Approve?",
      cell: ({ row }) => (
        <Checkbox
          checked={
            !!checked[
              `${row.original.dataset.title}-${row.original.paper.title}`
            ]
          }
          onChange={() =>
            handleCheck(
              `${row.original?.dataset.title}-${row.original?.paper.title}`
            )
          }
        />
      ),
    },
  ];

  const table = useReactTable({
    columns,
    data: rows,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    sorting,
    onSortingChange: setSorting,
    state: {
      sorting,
    },
  });

  const handleCheck = (paperId: string) => {
    setChecked((prev) => ({ ...prev, [paperId]: !prev[paperId] }));
  };

  return (
    <>
      <Box
        component="div"
        sx={{
          width: "100%",
          display: "flex",
          //justifyContent: "center",
          backgroundColor: "white",
          px: 2,
          borderBottom: "5px solid #3db28c",
        }}
      >
        <Link
          href="https://www.hdruk.ac.uk/"
          target="_blank"
          rel="noopener noreferrer"
          sx={{ display: "flex" }}
        >
          <Box
            component="img"
            src="https://www.hdruk.ac.uk/wp-content/uploads/2022/11/hdruk_main_rgb_jpeg-300x139.jpg"
            alt="HDR UK"
            sx={{
              maxHeight: "80px",
              height: "auto",
            }}
          />
        </Link>
      </Box>

      <Box
        sx={{
          backgroundColor: "#475da7",
          p: 5,
          width: "100%",
          minHeight: "100vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <Paper sx={{ width: "80%", overflow: "hidden", p: 3 }}>
          <Box>
            <Typography variant="h4">
              Review: Paper to Dataset Linkages
            </Typography>
          </Box>
          <TableContainer>
            <Table>
              <TableHead>
                {table.getHeaderGroups().map((headerGroup) => (
                  <TableRow key={headerGroup.id}>
                    {headerGroup.headers.map((header) => (
                      <TableCell
                        key={header.id}
                        sortDirection={header.column.getIsSorted()}
                      >
                        {header.isPlaceholder ? null : (
                          <TableSortLabel
                            active={!!header.column.getIsSorted()}
                            direction={
                              header.column.getIsSorted() === "desc"
                                ? "desc"
                                : "asc"
                            }
                            onClick={header.column.getToggleSortingHandler()}
                          >
                            {flexRender(
                              header.column.columnDef.header,
                              header.getContext()
                            )}
                          </TableSortLabel>
                        )}
                      </TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableHead>
              <TableBody>
                {table.getRowModel().rows.map((row) => (
                  <TableRow key={row.id}>
                    {row.getVisibleCells().map((cell) => (
                      <TableCell key={cell.id}>
                        {flexRender(
                          cell.column.columnDef.cell,
                          cell.getContext()
                        )}
                      </TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      </Box>
    </>
  );
}
