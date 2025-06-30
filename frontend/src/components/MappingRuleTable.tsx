import React from 'react';
import {
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    TextField,
    Select,
    MenuItem,
    FormControl,
} from '@mui/material';
import { MappingRule } from '../types/mapping';

interface MappingRuleTableProps {
    data: MappingRule[];
    onDataChange: (newData: MappingRule[]) => void;
}

const emptyRow: MappingRule = {
    styleNo: '',
    name: '',
    fabricType: '',
    category: '',
    gender: '',
    materialDetail: '',
    hsCode: '',
    note: '',
};

const MappingRuleTable: React.FC<MappingRuleTableProps> = ({ data, onDataChange }) => {
    // 데이터가 없으면 빈 행 5개 표시
    const displayData = data.length > 0 ? data : Array(5).fill(emptyRow);

    const handleCellChange = (rowIndex: number, field: keyof MappingRule, value: string) => {
        const newData = [...displayData];
        newData[rowIndex] = {
            ...newData[rowIndex],
            [field]: value
        };
        onDataChange(newData);
    };

    return (
        <TableContainer component={Paper} sx={{ mt: 2 }}>
            <Table size="small">
                <TableHead>
                    <TableRow>
                        <TableCell>StyleNo<br />(제품번호)</TableCell>
                        <TableCell>Name<br />(제품명)</TableCell>
                        <TableCell>FabricType<br />(knit / woven)</TableCell>
                        <TableCell>Category<br />(의류카테고리)</TableCell>
                        <TableCell>Gender<br />(men / women)</TableCell>
                        <TableCell>MaterialDetail<br />(소재 함유 상세)</TableCell>
                        <TableCell>HSCode</TableCell>
                        <TableCell>Note</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {displayData.map((row, rowIndex) => (
                        <TableRow key={rowIndex}>
                            <TableCell>
                                <TextField
                                    value={row.styleNo}
                                    onChange={(e) => handleCellChange(rowIndex, 'styleNo', e.target.value)}
                                    size="small"
                                    fullWidth
                                    variant="standard"
                                />
                            </TableCell>
                            <TableCell>
                                <TextField
                                    value={row.name}
                                    onChange={(e) => handleCellChange(rowIndex, 'name', e.target.value)}
                                    size="small"
                                    fullWidth
                                    variant="standard"
                                />
                            </TableCell>
                            <TableCell>
                                <FormControl fullWidth size="small">
                                    <Select
                                        value={row.fabricType}
                                        onChange={(e) => handleCellChange(rowIndex, 'fabricType', e.target.value)}
                                        variant="standard"
                                    >
                                        <MenuItem value="knit">knit</MenuItem>
                                        <MenuItem value="woven">woven</MenuItem>
                                    </Select>
                                </FormControl>
                            </TableCell>
                            <TableCell>
                                <TextField
                                    value={row.category}
                                    onChange={(e) => handleCellChange(rowIndex, 'category', e.target.value)}
                                    size="small"
                                    fullWidth
                                    variant="standard"
                                />
                            </TableCell>
                            <TableCell>
                                <FormControl fullWidth size="small">
                                    <Select
                                        value={row.gender}
                                        onChange={(e) => handleCellChange(rowIndex, 'gender', e.target.value)}
                                        variant="standard"
                                    >
                                        <MenuItem value="men">men</MenuItem>
                                        <MenuItem value="women">women</MenuItem>
                                    </Select>
                                </FormControl>
                            </TableCell>
                            <TableCell>
                                <TextField
                                    value={row.materialDetail}
                                    onChange={(e) => handleCellChange(rowIndex, 'materialDetail', e.target.value)}
                                    size="small"
                                    fullWidth
                                    variant="standard"
                                />
                            </TableCell>
                            <TableCell>
                                <TextField
                                    value={row.hsCode}
                                    onChange={(e) => handleCellChange(rowIndex, 'hsCode', e.target.value)}
                                    size="small"
                                    fullWidth
                                    variant="standard"
                                />
                            </TableCell>
                            <TableCell>
                                <TextField
                                    value={row.note}
                                    onChange={(e) => handleCellChange(rowIndex, 'note', e.target.value)}
                                    size="small"
                                    fullWidth
                                    variant="standard"
                                />
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
};

export default MappingRuleTable; 