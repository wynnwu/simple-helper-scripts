// Usage: node merge-folders.js

// Looks at the files in two different folders and copies them to a third folder,
// without copying any duplicates. Useful when you have two big folders, content
// may have been reorganized and added, and you want to deduplicate them.

// How it works:
// 1. Get all files from folder 1 and folder 2.
// 2. Calculate the MD5 hash of each file.
// 3. If the hash is not in the set of hashes, copy the file to the merged folder, add the hash to the list.
// 4. Repeat for all files.

const fs = require('fs');
const fsp = fs.promises;
const crypto = require('crypto');
const path = require('path');
const os = require('os');

async function getFileHash(filePath) {
    const hash = crypto.createHash('md5');
    const stream = fs.createReadStream(filePath);

    // Can handle larger files.
    return new Promise((resolve, reject) => {
        stream.on('data', chunk => {
            hash.update(chunk);
        });

        stream.on('end', () => {
            resolve(hash.digest('hex'));
        });

        stream.on('error', reject);
    });
}

async function getFilesFromDir(dir) {
    const filesToCheck = [];
    const items = await fsp.readdir(dir, { withFileTypes: true });

    for (const item of items) {
        // console.log('Processing: ', path.join(dir, item.name));
        if (item.isDirectory()) {
            const nestedFiles = await getFilesFromDir(path.join(dir, item.name));
            filesToCheck.push(...nestedFiles);
        } else {
            filesToCheck.push(path.join(dir, item.name));
        }
    }

    return filesToCheck;
}

async function mergeFoldersWithoutDuplicates(folder1, folder2, mergedFolder) {
    const filesFromFolder1 = await getFilesFromDir(folder1);
    const filesFromFolder2 = await getFilesFromDir(folder2);

    const fileHashes = new Set();

    for (const file of filesFromFolder1) {
        const fileHash = await getFileHash(file);
        if (!fileHashes.has(fileHash)) {
            console.log("Copying: ", path.join(mergedFolder, path.relative(folder1, file)));
            const destinationPath = path.join(mergedFolder, path.relative(folder1, file));
            // With recursive: true, if the directory already exists, it will not do anything.
            await fsp.mkdir(path.dirname(destinationPath), { recursive: true });
            await fsp.copyFile(file, destinationPath);
            fileHashes.add(fileHash);
        }
    }

    for (const file of filesFromFolder2) {
        const fileHash = await getFileHash(file);
        if (!fileHashes.has(fileHash)) {
            console.log("Copying: ", path.join(mergedFolder, path.relative(folder2, file)));
            const destinationPath = path.join(mergedFolder, path.relative(folder2, file));
            await fsp.mkdir(path.dirname(destinationPath), { recursive: true });
            await fsp.copyFile(file, destinationPath);
            fileHashes.add(fileHash);
        }
    }
}

// Make sure these folders exist already. 
const folder1Path = "PATH_TO_FOLDER1";
const folder2Path = "PATH_TO_FOLDER2";
const mergedFolderPath = "PATH_TO_MERGED_FOLDER";

mergeFoldersWithoutDuplicates(folder1Path, folder2Path, mergedFolderPath).then(() => {
    console.log('Merging completed.');
}).catch(error => {
    console.error('An error occurred:', error);
});
