from __future__ import annotations
import os
from typing import List

from sqlalchemy import create_engine, Column, String, Integer, BigInteger, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker, declarative_base

from ttlinks.macservice.oui_file_parsers import OuiFileParser, IEEEOuiCsvFile
from ttlinks.macservice.oui_utils import OUIUnit, OUIType

Base = declarative_base()
base_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources\\')

class OUIDB(Base):
    """
    SQLAlchemy model for storing OUI (Organizationally Unique Identifier) records in the database.

    Attributes:
        oui_id (str): The OUI identifier (6-character prefix).
        start_hex (str): Start hexadecimal value of the OUI range.
        end_hex (str): End hexadecimal value of the OUI range.
        start_decimal (int): Start decimal representation of the OUI range.
        end_decimal (int): End decimal representation of the OUI range.
        block_size (int): The block size allocated for this OUI range.
        oui_type (str): The type of OUI (IAB, MA_S, MA_M, etc.).
        organization (str): Organization associated with the OUI.
        address (str): Organization's address.
    """

    __tablename__ = 'OUIDB'

    oui_id = Column(String(6))
    start_hex = Column(String(6))
    end_hex = Column(String(6))
    start_decimal = Column(BigInteger, index=True)
    end_decimal = Column(BigInteger, index=True)
    block_size = Column(Integer)
    oui_type = Column(String(10))
    organization = Column(String(150))
    address = Column(String(500))

    __table_args__ = (
        PrimaryKeyConstraint('oui_id', 'start_decimal', 'end_decimal'),
    )

class OUIDBLoader:
    """
    Manages database connection and session creation.

    Attributes:
        _engine: SQLAlchemy engine for database operations.
        _SessionFactory: SQLAlchemy session factory.
    """
    def __init__(self, db_url: str="sqlite:///oui.db"):
        """
        Initializes the database engine and session factory.

        Args:
            db_url (str): The database URL (default is SQLite database `oui.db`).
        """
        self._engine = create_engine(
            db_url,
            echo=False,
            connect_args={"check_same_thread": False}
        )
        self._SessionFactory = sessionmaker(bind=self._engine)
        self.__init_db()

    def __init_db(self):
        """Creates database tables if they do not exist."""
        Base.metadata.create_all(self._engine)

    @property
    def create_session(self):
        """Returns a new database session."""
        return self._SessionFactory()

    @property
    def engine(self):
        """Returns the database engine."""
        return self._engine


class OUIDBUpdater:
    """
    Handles updating the OUI database by parsing official OUI files.

    Attributes:
        _loader (OUIDBLoader): Database loader instance.
        _official_files (List): List of OUI files to be processed.
        _oui_parsers: OUI file parser class.
    """

    def __init__(
            self,
            loader: OUIDBLoader,
            official_files: List = None
    ):
        """
        Initializes the OUIDBUpdater.

        Args:
            loader (OUIDBLoader): Database loader instance.
            official_files (List, optional): List of official OUI files to be processed.
        """
        if official_files is None:
            self._official_files = [
                IEEEOuiCsvFile(os.path.join(base_folder, 'default_cid.csv')),
                IEEEOuiCsvFile(os.path.join(base_folder, 'default_iab.csv')),
                IEEEOuiCsvFile(os.path.join(base_folder, 'default_mas.csv')),
                IEEEOuiCsvFile(os.path.join(base_folder, 'default_mam.csv')),
                IEEEOuiCsvFile(os.path.join(base_folder, 'default_mal.csv')),
            ]
        else:
            self._official_files = official_files
        self._loader = loader
        self._oui_parsers = OuiFileParser

    def _parse_oui_file(self):
        """
        Parses OUI files and extracts OUI records.

        Returns:
            List[Dict]: List of dictionaries containing OUI record data.
        """
        oui_units = []
        for files in self._official_files:
            oui_units.extend(OuiFileParser.parse_oui_file(files)['oui_units'])
        return [oui_unit.record for oui_unit in oui_units]

    def batch_upsert(self):
        """
        Performs batch update and insert operations in the OUI database.
        Ensures unique records are updated instead of duplicated.
        """
        data = self._parse_oui_file()
        for d in data:
            d["start_decimal"] = int(d["start_decimal"])
            d["end_decimal"] = int(d["end_decimal"])

        unique_data_map = {}
        for d in data:
            key = (d["oui_id"], d["start_decimal"], d["end_decimal"])
            if key not in unique_data_map:
                unique_data_map[key] = d
        clean_data = list(unique_data_map.values())

        session = self._loader.create_session
        existing_pks = {
            (row.oui_id, row.start_decimal, row.end_decimal)
            for row in session.query(OUIDB.oui_id, OUIDB.start_decimal, OUIDB.end_decimal).all()
        }

        updates = [d for d in clean_data if (d["oui_id"], d["start_decimal"], d["end_decimal"]) in existing_pks]
        inserts = [d for d in clean_data if (d["oui_id"], d["start_decimal"], d["end_decimal"]) not in existing_pks]

        print(f"Updating {len(updates)} records...")
        print(f"Inserting {len(inserts)} new records...")

        if updates:
            session.bulk_update_mappings(OUIDB.__mapper__, updates)
            session.commit()

        if inserts:
            session.bulk_insert_mappings(OUIDB.__mapper__, inserts)
            session.commit()


class OUIDBSearcher:
    """
    Implements binary search to find OUI records by decimal value.

    Attributes:
        _loader (OUIDBLoader): Database loader instance.
        _records (List[OUIDB]): Sorted list of OUI records for fast searching.
    """
    def __init__(self, loader: OUIDBLoader):
        """
        Initializes the OUI database searcher and preloads records.

        Args:
            loader (OUIDBLoader): Database loader instance.
        """
        self._loader = loader

        with self._loader.create_session as session:
            all_records = session.query(OUIDB).all()

        self._records = sorted(all_records, key=lambda rec: rec.start_decimal)

    def search_by_decimal(self, decimal_value: int):
        """
        Searches for OUI records based on decimal value using binary search.

        Args:
            decimal_value (int): The decimal representation of a MAC address.

        Returns:
            List[OUIUnit]: List of matching OUI records.
        """
        return self._binary_search(decimal_value)

    def _binary_search(self, decimal_value: int) -> list[OUIUnit]:
        """
        Implements binary search to find OUI records by decimal value.

        Args:
            decimal_value (int): The decimal representation of a MAC address.

        Returns:
            List[OUIUnit]: List of matching OUI records.
        """
        left = 0
        right = len(self._records) - 1
        results = []

        while left <= right:
            mid = (left + right) // 2
            mid_record = self._records[mid]

            if decimal_value < mid_record.start_decimal:
                right = mid - 1
            elif decimal_value > mid_record.end_decimal:
                left = mid + 1
            else:
                results.append(self._to_oui_unit(mid_record))

                scan_left = mid - 1
                while scan_left >= 0:
                    r = self._records[scan_left]
                    if r.start_decimal <= decimal_value <= r.end_decimal:
                        results.append(self._to_oui_unit(r))
                        scan_left -= 1
                    else:
                        break

                scan_right = mid + 1
                while scan_right < len(self._records):
                    r = self._records[scan_right]
                    if r.start_decimal <= decimal_value <= r.end_decimal:
                        results.append(self._to_oui_unit(r))
                        scan_right += 1
                    else:
                        break
                break

        return results

    def _to_oui_unit(self, record: OUIDB) -> OUIUnit:
        """Converts an OUIDB record into an OUIUnit object."""
        return OUIUnit(
            oui_id=record.oui_id,
            start_hex=record.start_hex,
            end_hex=record.end_hex,
            block_size=record.block_size,
            oui_type=OUIType[record.oui_type],
            organization=record.organization,
            address=record.address
        )