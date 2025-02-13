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
  const response = await fetch("http://localhost:8000/find/via-abstracts");
  const data = await response.json();
  return data;
};

export const meta: MetaFunction = () => [
  { title: "New Remix App" },
  { name: "description", content: "Welcome to Remix!" },
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

  const [sorting, setSorting] = useState<SortingState>([]);

  const columns: ColumnDef<DataItem[]> = [
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
      id: "Score",
      cell: (info) => info.getValue(),
      header: () => <> Score </>,
    },
    {
      id: "approve",
      header: "Approve?",
      cell: ({ row }) => (
        <Checkbox
          checked={!!checked[row.original?.paper.id]}
          onChange={() => handleCheck(row.original?.paper.id)}
        />
      ),
    },
  ];

  //const columnHelper = createColumnHelper<DataItem>();
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
    <Box
      sx={{
        backgroundColor: "#d0e8ff",
        p: 5,
        width: "100%",
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Paper sx={{ width: "80%", overflow: "hidden", p: 3 }}>
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
  );
}
